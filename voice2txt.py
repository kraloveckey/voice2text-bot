#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import telebot
import requests
import speech_recognition as sr
import subprocess
import datetime

logfile = str(datetime.date.today()) + '.log'
token = 'TOKEN_BOT'
bot = telebot.TeleBot(token)

def audio_to_text(dest_name: str):
# Function for translation of audio, in the format .vaw in the text.
    r = sr.Recognizer()
    # Read our .vaw file.
    message = sr.AudioFile(dest_name)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language="ru_RU") # Here you can change the recognition language.
    return result

@bot.message_handler(content_types=['voice'])
def get_audio_messages(message):
# The main function that takes a voice from the user.
    try:
        print("Started recognition...")
        # Below we try to extract the name of the file, and in general we take data from the Telegram message.
        file_info = bot.get_file(message.voice.file_id)
        path = os.path.splitext(file_info.file_path)[0] # This is the full path to the file (for example: voice/file_2.oga)
        fname = os.path.basename(path) # We convert the path to the file name (for example: file_2.oga)
        # We get and save the sent voice message.
        # The admin can at any time turn off the removal of audio files and listen to everything that you say there. 
        # Imagine that this is hooked into a huge chat and it will simply logging all messages [anonymity in a telegram, lol])
        doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        with open(fname+'.oga', 'wb') as f:
            f.write(doc.content) # Here the audio-message is saved.
        process = subprocess.run(['ffmpeg', '-i', fname+'.oga', fname+'.wav']) # It is used here ffmpeg to convert .oga in .vaw.
        result = audio_to_text(fname+'.wav') # Call the function for transferring audio to text, and at the same time we transfer the names of files for their subsequent deletion.
        bot.send_message(message.chat.id, format(result))
    except sr.UnknownValueError as e:
        bot.send_message(message.chat.id, "Прошу прощения, но я не разобрал сообщение, прочистите рот или же оно пустое...")
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) + ':Message is empty.\n')
    except Exception as e:
        bot.send_message(message.chat.id, "Что-то пошло через жопу, но наши смелые инженеры уже трудятся над решением... \nДа ладно, никто эту ошибку исправлять не будет, она просто потеряется в логах.")
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) +':' + str(e) + '\n')
    finally:
        os.remove(fname+'.wav')
        os.remove(fname+'.oga')

bot.polling(none_stop=True, interval=0) # We very unculturally knock on the telegram and check the availability of messages.