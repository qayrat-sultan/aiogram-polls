from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.exceptions import BotBlocked, BotKicked, UserDeactivated

import configs

from aiogram import types
from main import bot


async def menu_handler(message: types.Message):
    await message.answer("Main menu")


async def start_menu_handler(m: types.Message):
    if configs.collusers.count_documents({"_id": m.from_user.id}) == 0:
        # Adding new user DB
        configs.collusers.insert_one({"_id": m.from_user.id,
                                      "username": m.from_user.username,
                                      "first_name": m.from_user.first_name,
                                      "last_name": m.from_user.last_name})
    elif configs.collusers.count_documents(
            {"_id": m.from_user.id, "status": False}) == 1:
        configs.collusers.update_one(
            {"_id": m.from_user.id}, {"$set": {"status": True}})
    else:
        configs.collusers.update_one(
            {"_id": m.from_user.id}, {"$set": {"status": True}})
    await m.answer("🏠 Main menu")


async def some_text_handler(message: types.Message):
    if message.chat.id == configs.GROUP_ID and message.reply_to_message:
        report_data = configs.collreports.find_one({
            "group_msg_id": message.reply_to_message.message_id})
        try:
            await bot.send_message(report_data['user_id'],
                                   message.text,
                                   entities=message.entities,
                                   reply_to_message_id=report_data.get(
                                       'bot_msg_id'
                                   ))
        except (TypeError, BotBlocked, BotKicked,
                UserDeactivated, Exception) as e:
            configs.collusers.delete_one({"_id": report_data['user_id']})
            await message.answer(e)
    else:
        await message.answer("I'll answer for u")
        answer_dict = configs.collanswers.find_one({"user_id": message.from_user.id,
                                                    "status": False})
        if answer_dict:
            await bot.delete_message(answer_dict['user_id'], answer_dict['msg_id'])
            configs.collanswers.delete_one({"msg_id": answer_dict['msg_id']})
        question = await get_unanswered_question(message.from_user.id)
        if question:
            x = await message.answer_poll(question['question'], question['answers'], is_anonymous=False)
            configs.collanswers.insert_one({"msg_id": x.message_id,
                                            "user_id": x.chat.id,
                                            "question": question['number'],
                                            "status": False})


async def get_unanswered_question(user_id):
    answer = configs.collanswers.find_one({"user_id": user_id})
    if not answer:
        question = configs.collquestions.find_one({"number": 1})
    else:
        questions = configs.collquestions.count_documents({})
        if answer['question'] < questions:
            question = configs.collquestions.find_one({"number": answer['question']+1})
        else:
            question = None
    return question


async def report_process_handler(message: types.Message,
                                 state: FSMContext):
    async with state.proxy() as data:
        if message.text == "✅ Submit":
            await message.answer("Sended!")
            if data['message'].content_type == 'voice':
                m = await bot.send_voice(chat_id=configs.GROUP_ID,
                                         voice=data['message'].voice.file_id,
                                         caption=data['message'].caption,
                                         caption_entities=data.get(
                                             'message').caption_entities)
                configs.collreports.insert_one({
                    "group_msg_id": m.message_id,
                    "bot_msg_id": data['message'].message_id,
                    "user_id": m.from_user.id
                })
            elif data['message'].content_type == 'video':
                m = await bot.send_video(chat_id=configs.GROUP_ID,
                                         video=data['message'].video,
                                         caption=data['message'].caption)
                configs.collreports.insert_one({
                    "group_msg_id": m.message_id,
                    "bot_msg_id": data['message'].message_id,
                    "user_id": m.from_user.id
                })
            elif data['message'].content_type == 'photo':
                m = await bot.send_photo(chat_id=configs.GROUP_ID,
                                         photo=data.get(
                                             'message').photo[-1].file_id,
                                         caption=data['message'].caption)
                configs.collreports.insert_one({
                    "group_msg_id": m.message_id,
                    "bot_msg_id": data['message'].message_id,
                    "user_id": m.from_user.id
                })
            elif data['message'].content_type == 'sticker':
                m = await bot.send_sticker(chat_id=configs.GROUP_ID,
                                           sticker=data.get(
                                               'message').sticker.file_id)
                configs.collreports.insert_one({
                    "group_msg_id": m.message_id,
                    "bot_msg_id": data['message'].message_id,
                    "user_id": m.from_user.id
                })
            elif data['message'].content_type == 'text':
                m = await bot.send_message(chat_id=configs.GROUP_ID,
                                           text=data['message'].text)
                configs.collreports.insert_one({
                    "group_msg_id": m.message_id,
                    "bot_msg_id": data['message'].message_id,
                    "user_id": data['message'].from_user.id
                })
            elif data['message'].content_type == 'document':
                m = await bot.send_document(chat_id=configs.GROUP_ID,
                                            document=data.get(
                                                'message').document.file_id)
                configs.collreports.insert_one({
                    "group_msg_id": m.message_id,
                    "bot_msg_id": data['message'].message_id,
                    "user_id": m.from_user.id
                })
            await state.finish()
            await menu_handler(message)
        elif message.text == "🏠 Main menu":
            await state.finish()
            await menu_handler(message)
        else:
            data['message'] = message
            keyboard = ReplyKeyboardMarkup(
                [[KeyboardButton("✅ Submit"), KeyboardButton("🏠 Main menu")
                  ]], resize_keyboard=True, one_time_keyboard=True)
            await message.answer("Send?", reply_markup=keyboard)


async def poll_answers_handler(poll: types.PollAnswer):
    print("МАНА САНГА УША КАЙФ", poll)
    answer_dict = configs.collanswers.find_one({"user_id": poll.user.id, "status": False})
    print(answer_dict)
    if answer_dict:
        if poll.user.id == answer_dict['user_id']:
            print(poll.option_ids)
            await bot.stop_poll(poll.user.id, answer_dict['msg_id'])
            configs.collanswers.update_one({"msg_id": answer_dict['msg_id']},
                                           {"$set": {"status": True, "answer": poll.option_ids}})
            next_question = await get_unanswered_question(answer_dict['user_id'])
            print("DADA", next_question)
            if next_question:
                await bot.send_poll(answer_dict['user_id'], next_question['question'], next_question['answers'],
                                    is_anonymous=False)
        else:
            await bot.delete_message(answer_dict, answer_dict['user_id'])
            await bot.send_message(answer_dict, "Faqat o'zigniz ovoz berishingiz kerak! "
                                                "Boshqalar ovozi hisoblanmaydi!")
            await bot.send_poll(answer_dict, "Savol", ["Javob", "2-chi javob"], is_anonymous=False)
