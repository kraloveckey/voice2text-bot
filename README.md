# voice2text-bot

Telegram bot written on Python that convert Telegram voice message to text message. 

## Install dependencies

```bash
sudo apt install ffmpeg or brew install ffmpeg
pip3 install -r requirements.txt
```

## Create a Telegram bot

Write to the account `@BotFather` the message `/newbot` and follow the
instructions. Enter the retreived token to the `token` property in `voice2txt.py` file.

## Create a Telegram group

Create a Telegram group and add your created bot as an admin without any
privileges.

## Run the script

```bash
cd voice2text-bot
python3 voice2text.py
```