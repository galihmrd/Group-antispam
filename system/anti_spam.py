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
    try:
       try:
          toCheck.index("BTC")
       except ValueError:
          pass
       try:
          toCheck.index("blockchain")
       except ValueError:
          pass
       try:
          toCheck.index("ETH")
       except ValueError:
          pass
       try:
          toCheck.index("Elon musk")
       except ValueError:
          pass
       await message.reply("Spam detected!\nBanned user!")
    except Exception as e:
       await message.reply(e)
