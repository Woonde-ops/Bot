import requests
import os
import time

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import bot, KEYID, KEYSECRET

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Можно начинать')


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Ты попал в краткую сводку о боте. Бот расшифровывает твои ГС и кружочки =D')


@router.message()
async def voice(message: Message):
    if message.voice:
        ms = await message.reply('Сообщение принято...')
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_name = f'C:/Users/ольга/Downloads/{file_id}.mp3'
        await bot.download_file(file_path, file_name)

        headers = {'KeyID': KEYID, 'KeySecret': KEYSECRET}
        create_url = "https://api.speechflow.io/asr/file/v1/create?lang=ru"  
        query_url = "https://api.speechflow.io/asr/file/v1/query?taskId="
        file_in = open(file_name, 'rb')
        files = {'file': file_in}


        response = requests.post(create_url, headers=headers, files=files)
        if response.status_code == 200:
            create_result =response.json()
            query_url += create_result['taskId'] + "&resultType=4"

            while True:
                response = requests.get(query_url, headers=headers)

                if response.status_code == 200:
                    query_result = response.json() 
                    if query_result['code'] == 11000:
                        if query_result['result']:
                            result = query_result['result'].replace('\n\n', ' ')
                            await ms.edit_text(f'<pre><code>{result}</code></pre>',parse_mode='html')
                            file_in.close()
                            os.remove(file_name)
                        break
                    elif query_result['code'] == 11001:
                        time.sleep(3)
                        continue
                    else:
                        break
                else:
                    break
    