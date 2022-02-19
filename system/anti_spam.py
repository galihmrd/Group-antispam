import os

import pytesseract
import requests
from PIL import Image
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from pyrogram.types import Message


@Client.on_message(filters.photo)
async def antispam(client, message):
    userID = message.from_user.id
    chatID = message.chat.id
    fileID = str(message.photo.file_id)
    langCode = "eng"
    dbUrl = f"https://github.com/galihmrd/tessdata/raw/main/{langCode}.traineddata"
    dirs = r"./vendor/data/tessdata"
    path = os.path.join(dirs, f"{langCode}.traineddata")
    if not os.path.exists(path):
        data = requests.get(
            dbUrl, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}
        )
        if data.status_code == 200:
            open(path, "wb").write(data.content)
        else:
            return await message.reply("Something is wrong")
    try:
       inputImage = await client.download_media(fileID)
       openImage = Image.open(inputImage)
       outputText = pytesseract.image_to_string(openImage, lang=f"{langCode}")
    except Exception as e:
       await message.reply(e)
    toCheck = outputText[:-1]
    banWords = "BTC ETH blockchain bitcoin cryptocurrency"
    finalWords = banWords.split()
    for x in finalWords:
        if x in toCheck:
            banMsg = await message.reply("Spam detected!\nBanning user...")
            try:
               await client.ban_chat_member(chatID, userID)
               await banMsg.edit(f"Banned {userID}!")
            except Exception as e:
               await banMsg.edit(e)
