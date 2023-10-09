from setuptools import setup

setup(
    name='checkpwned-telegram-bot',
    version='1.0.0',
    description='A Telegram bot for checking if an email or password has been pwned',
    author='Ethan Lacerenza',
    scripts=['hib-bot.py'],
    install_requires=[
        'requests',
        'python-telegram-bot'
        'logging'
    ],
)