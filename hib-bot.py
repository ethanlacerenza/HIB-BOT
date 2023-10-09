import requests
import telebot

# Define your Telegram Bot API token (you can obtain this from BotFather on Telegram)
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Define your Have I Been Pwned API key
HIBP_API_KEY = 'YOUR_HIBP_API_KEY'

# Create a Telegram bot object
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Define a command handler for the /checkpwned command
@bot.message_handler(commands=['checkpwned'])
def check_pwned(message):
    try:
        # Get the user's input
        user_input = message.text.split(" ", 1)[1]

        # Construct the API URL to check if an email or password has been pwned
        api_url = f'https://haveibeenpwned.com/api/v3/{user_input}'

        # Set up the headers with the Have I Been Pwned API key
        headers = {
            'hibp-api-key': HIBP_API_KEY
        }

        # Send a GET request to the Have I Been Pwned API
        response = requests.get(api_url, headers=headers)

        # Log the request and response details in the chat
        log_message = f'Request URL: {api_url}\nResponse Code: {response.status_code}\nResponse Content: {response.text}'
        bot.reply_to(message, log_message)

        # Check the response status code
        if response.status_code == 200:
            result_message = f'{user_input} has been pwned {response.text} times.'
        elif response.status_code == 404:
            result_message = f'{user_input} has not been pwned.'
        else:
            result_message = 'An error occurred while checking the pwned status.'

        # Send the result message back to the user
        bot.reply_to(message, result_message)

    except IndexError:
        # Handle the case where the user didn't provide an input
        bot.reply_to(message, 'Please provide an email or password to check.')

# Start the Telegram bot
bot.polling()
