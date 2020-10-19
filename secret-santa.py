from twilio.rest import Client
import random
import csv
import yaml
import sys


def get_client(config_file):
    with open(config_file) as f:
        conf = yaml.load(f, Loader=yaml.Loader)

        # get twilio client object and phone number
        client = Client(conf['client_sid'], conf['client_token'])
        twilio_num = conf['twilio_num']
    
    config_dict = {
        'client_obj': client,
        'twilio_num': twilio_num
    }
    return config_dict


def get_numbers_dict(input_file):
    """
    load in CSV file of names and phone numbers
    return as dictionary
    """
    numbers_dict = {}
    with open(input_file) as f:
        reader = csv.reader(f)

        for name, number in reader:
            # check phone number is valid
            assert len(number) == 13
            assert number.startswith('+44')

            # add to dict
            numbers_dict[name] = number

    return numbers_dict


def secret_santa(numbers_dict):
    """
    Generates a list of secret santa matches
    """
    # declare empty lists for storing results
    used_list = []
    decision_list = []

    # make a list of all secret santas and shuffle it
    santa_list = list(numbers_dict.keys())
    random.shuffle(santa_list)

    for santa in santa_list:
        # make a new copy of all people in the list
        available_list = list(numbers_dict.keys())

        # remove the secret santa and anyone who has already been selected
        available_list.remove(santa)
        for used in used_list:
            if used in available_list:
                available_list.remove(used)

        # make a choice from the remaining people
        selection = random.choice(available_list)
        used_list.append(selection)

        # add choice to the results list - phone_num, from, to
        decision_list.append(
            (numbers_dict[santa], santa, selection)
        )
        
    return decision_list


def send_msg(santa_num, santa_from, santa_to, config):
    """
    Sends a text message to the santa saying who they have been picked
    """
    # unpack config
    client = config['client_obj']
    twilio_num = config['twilio_num']

    # write message
    message = f"Merry Xmas {santa_from}!\nYour secret dick'ed this year is {santa_to}.\nHohoho! *<I:^)>>"

    # send message
    client.messages.create(
        to    = santa_num, 
        from_ = twilio_num, 
        body  = message
    )



if __name__ == '__main__':
    numbers_file = sys.argv[1]
    config_file = sys.argv[2]

    # load config and phone numbers
    config = get_client(config_file)
    numbers_dict = get_numbers_dict(numbers_file)
    
    # make the secret santa list
    santa_list = secret_santa(numbers_dict)

    # send texts
    for entry in santa_list:
        phone_num, santa_from, santa_to = entry
        #send_msg(phone_num, santa_from, santa_to, config)

    # make hard copy
    with open('DO_NOT_OPEN__Secret_Santa.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(santa_list)
