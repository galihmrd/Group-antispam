import os
from pyrogram import Client, filters
from pyrogram.types import Message

from nudenet import NudeDetector


@Client.on_message(filters.photo)
async def anti_nsfw(client, filters):
    userMention = message.from_user.mention
    fileID = str(message.photo.file_id)
    detector = NudeDetector()
    try:
       inputFile = await client.download_media(fileID)
       await message.delete()
       detector.censor(
           inputFile,
           out_path=f'./{message.chat.id}_out.jpg',
           visualize=False
       )
       await message.reply_photo(
            photo=f'./{message.chat.id}_out.jpg',
            caption=f'**Sender:** {userMention}'}
       )
       os.remove(f'./{message.chat.id}_out.jpg')
    except Exception as e:
       await message.reply(e)
