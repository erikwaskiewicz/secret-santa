# Secret Santa generator

Needlessly complicated secret santa generator. 

Uses Twilio to send the results via text, because my family don't have emails and there doesn't seem to be an app that sends out texts.

## Requirements

### 1. Set up a Twilio account

Tutorial - https://www.twilio.com/docs/sms/quickstart/python

You'll need to buy some Twilio credit and buy a number to send from (you can remove this afterwards, otheriwse there will be a monthly cost)

### 2. Make a YAML config for your Twilio account

Example config:
```
client_sid: 'ABCDEFG1234567890'
client_token: '1234567890ABCDEFG'
twilio_num: '+440000000000'
```
These details are from your Twilio account

### 3. Make a CSV with the names and numbers of each person to be included

Must follow this format, numbers must begin with +44
```
person1,+441111111111
person2,+442222222222
person3,+443333333333
```

### 4. Install Conda env

`conda install -f env.yml`

### 5. Run the program

`python secret-santa.py <path_to_phone_numbers_file> <path_to_config_file>`

Texts will be sent automatically. The matches will be saved to a file called `DO_NOT_OPEN__Secret_Santa.csv`, don't open this if you want to keep it secret!
