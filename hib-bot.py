#!/usr/bin/env python3
import requests
import telebot
import logging  # Importa il modulo logging

# Configura il logging per registrare gli output sulla console
logging.basicConfig(level=logging.DEBUG)

TELEGRAM_BOT_TOKEN = ''
CHAT_ID = ''
# Define your Have I Been Pwned API key
HIBP_API_KEY = ''

# Create a Telegram bot object
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Define a command handler for the /checkpwned command
@bot.message_handler(commands=['checkpwned'])
def check_pwned(message):
    try:
        # Get the user's input (email)
        user_input = message.text.split(" ", 1)[1]

        # Construct the API URL to check if an email has been pwned
        api_url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{user_input}'

        # Set up the headers with the Have I Been Pwned API key
        headers = {
            'hibp-api-key': HIBP_API_KEY
        }

        # Send a GET request to the Have I Been Pwned API
        response = requests.get(api_url, headers=headers)

        # Log the request and response details
        logging.debug(f'Request URL: {api_url}')
        logging.debug(f'Response Code: {response.status_code}')
        logging.debug(f'Response Content: {response.text}')

        # Check the response status code
        if response.status_code == 200:
            breaches = response.json()
            if breaches:
                result_message = f'{user_input} has been pwned in the following breaches:\n'
                for breach in breaches:
                    result_message += f'- {breach["Name"]}\n'
            else:
                result_message = f'{user_input} has not been pwned.'
        elif response.status_code == 404:
            result_message = f'{user_input} has not been pwned.'
        else:
            result_message = 'An error occurred while checking the pwned status.'

        # Send the result message back to the user
        bot.send_message(CHAT_ID, result_message)

    except IndexError:
        # Handle the case where the user didn't provide an email
        bot.send_message(CHAT_ID, 'Please provide an email to check.')

# Start the Telegram bot
bot.polling()
