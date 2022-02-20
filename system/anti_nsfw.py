import os
from pyrogram import Client, filters
from pyrogram.types import Message

from nudenet import NudeDetector

try:
   detector = NudeDetector()
except BaseException:
   pass

@Client.on_message(filters.photo)
async def anti_nsfw(client, message):
    userMention = message.from_user.mention
    fileID = str(message.photo.file_id)
    inputFile = await client.download_media(fileID)
    try:
       detector.censor(
           inputFile,
           out_path=f'./{message.chat.id}_out.jpg',
           visualize=False
       )
       await message.reply_photo(
            photo=f'./{message.chat.id}_out.jpg',
            caption=f'**Sender:** {userMention}',
       )
       os.remove(f'./{message.chat.id}_out.jpg')
       await message.delete()
    except Exception as e:
       await message.reply(e)
