import configs
import asyncio
import logging
from aiogram.utils.exceptions import BotKicked, BotBlocked, UserDeactivated
from aiogram import Bot, types


async def user_statistics(message: types.Message):
    x = configs.collusers.find()
    await message.answer(f"Users: {len(x)}")


async def send_post_all_users(data: dict, users: tuple, bot: Bot):
    if data['type'] == 'voice':
        for i in users:
            try:
                await bot.send_voice(chat_id=i,
                                     voice=data['voice'],
                                     caption=data['caption'],
                                     caption_entities=data['caption_entities'])
                await asyncio.sleep(0.04)
            except (BotKicked, BotBlocked, UserDeactivated):
                await user_blocked_with_posting(i)
    elif data['type'] == 'text':
        for i in users:
            try:
                await bot.send_message(chat_id=i,
                                       text=data['text'],
                                       entities=data['entities'])
                await asyncio.sleep(0.04)
            except (BotKicked, BotBlocked, UserDeactivated):
                await user_blocked_with_posting(i)
    elif data['type'] == 'video':
        for i in users:
            try:
                await bot.send_video(chat_id=i,
                                     video=data['video'],
                                     caption=data['caption'],
                                     caption_entities=data['caption_entities'])
                await asyncio.sleep(0.04)
            except (BotKicked, BotBlocked, UserDeactivated):
                await user_blocked_with_posting(i)
    elif data['type'] == 'photo':
        for i in users:
            try:
                await bot.send_photo(chat_id=i,
                                     photo=data['photo'],
                                     caption=data['caption'],
                                     caption_entities=data['caption_entities'])
                await asyncio.sleep(0.04)
            except (BotKicked, BotBlocked, UserDeactivated):
                await user_blocked_with_posting(i)
    elif data['type'] == 'sticker':
        for i in users:
            try:
                await bot.send_sticker(chat_id=i,
                                       sticker=data['sticker'])
                await asyncio.sleep(0.04)
            except (BotKicked, BotBlocked, UserDeactivated):
                await user_blocked_with_posting(i)
    elif data['type'] == 'document':
        for i in users:
            try:
                await bot.send_document(chat_id=i,
                                        document=data['document'],
                                        caption=data['caption'],
                                        caption_entities=data.get(
                                            'caption_entities'))
                await asyncio.sleep(0.04)
            except (BotKicked, BotBlocked, UserDeactivated):
                await user_blocked_with_posting(i)


async def user_blocked_with_posting(user: int):
    configs.collusers.update_one({"_id": user}, {"$set": {"status": False}})
    logging.warning(f"This {user} user id was are blocked the bot")
