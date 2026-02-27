import asyncio
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, field
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
BOT_TOKEN = 'bot token'
GROUP_ID = 'group id'
MODERATION_TOPIC_ID = 'topic id'
bot=Bot(token=BOT_TOKEN)
storage=MemoryStorage()
dp=Dispatcher(storage=storage)
user_topics:Dict[int,int]={}
topic_to_user:Dict[int,int]={}
class FSMStates(StatesGroup):
    single_q1=State();single_q2=State();single_q3=State();single_q4=State();single_q5=State();single_q6=State();single_q7=State();single_q8=State();single_q9=State();single_q10=State();single_q11=State();single_q12=State();single_q13=State();single_q14=State();single_q15=State();single_q16=State();single_q17=State();single_q18=State();single_q19=State();single_q20=State();single_q21=State();single_q22=State();single_confirm=State()
    album_q1=State();album_q2=State();album_q3=State();album_q4=State();album_q5=State();album_q6=State();album_q7=State();album_q8=State();album_q9=State();album_q10=State();album_q11=State();album_q12=State();album_q13=State();album_q14=State();album_q15=State();album_q16=State();album_q17=State();album_q18=State();album_q19=State();album_q20=State();album_confirm=State()
    mod_reject_reason=State()
def main_menu_kb():return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отправить релиз")],[KeyboardButton(text="Позвать модератора")]],resize_keyboard=True)
def cancel_back_kb():return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Назад"),KeyboardButton(text="Отмена")]],resize_keyboard=True)
def single_q1_kb():return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Уже были релизы")],[KeyboardButton(text="Это первый релиз")],[KeyboardButton(text="Отмена")]],resize_keyboard=True)
def single_q2_kb():return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Сингл")],[KeyboardButton(text="Альбом/EP")],[KeyboardButton(text="Отмена")]],resize_keyboard=True)
def single_q3_ready_kb():return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Я готов(-а) выгружать релиз")],[KeyboardButton(text="Отмена")]],resize_keyboard=True)
def yes_no_kb():return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Да"),KeyboardButton(text="Нет")],[KeyboardButton(text="Назад"),KeyboardButton(text="Отмена")]],resize_keyboard=True)
def zero_kb():return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="0")],[KeyboardButton(text="Назад"),KeyboardButton(text="Отмена")]],resize_keyboard=True)
def confirm_kb():return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отправить на модерацию")],[KeyboardButton(text="Отмена")]],resize_keyboard=True)
def skip_only_kb():return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Пропустить")],[KeyboardButton(text="Назад"),KeyboardButton(text="Отмена")]],resize_keyboard=True)
def mod_actions_kb(user_id:int):return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Одобрить релиз",callback_data=f"mod_approve:{user_id}")],[InlineKeyboardButton(text="Отказать",callback_data=f"mod_reject:{user_id}")]])
async def send_and_log(user_id:int,text:str,reply_markup=None,**kwargs):
    await bot.send_message(user_id,text,reply_markup=reply_markup,**kwargs)
    if user_id not in user_topics:
        try:
            chat=await bot.get_chat(user_id)
            username=chat.username
            topic_name=f"{user_id} ({username})" if username else str(user_id)
            topic=await bot.create_forum_topic(GROUP_ID,name=topic_name)
            user_topics[user_id]=topic.message_thread_id
            topic_to_user[topic.message_thread_id]=user_id
        except:return
    try:await bot.send_message(GROUP_ID,f"{text}\n\n\nнаписал бот",message_thread_id=user_topics[user_id],disable_notification=True)
    except:pass
async def log_user_response(user_id:int,text:str):
    if user_id in user_topics:
        try:await bot.send_message(GROUP_ID,f"Пользователь ответил: {text}",message_thread_id=user_topics[user_id],disable_notification=True)
        except:pass
async def reset_to_main_menu(message:Message,state:FSMContext):
    await state.clear()
    await send_and_log(message.from_user.id,"Главное меню:",reply_markup=main_menu_kb())
@dp.message(Command("start"),F.chat.type=="private")
async def cmd_start(message:Message,state:FSMContext):
    await state.clear()
    await send_and_log(message.from_user.id,"Главное меню:",reply_markup=main_menu_kb())
@dp.message(F.text=="Позвать модератора",F.chat.type=="private")
async def call_moderator(message:Message,state:FSMContext):
    await state.clear()
    user_id=message.from_user.id
    if user_id not in user_topics:await send_and_log(user_id,"Создание темы...")
    topic_id=user_topics.get(user_id)
    if topic_id:await bot.send_message(GROUP_ID,"@clockerka человек позвал модератора",message_thread_id=topic_id,disable_notification=True)
    await send_and_log(user_id,"Уже спешим на помощь! Пока что пожалуйста, напишите в чат вашу проблему, и мы постараемся ее решить максимально оперативно!",reply_markup=main_menu_kb())
@dp.message(F.text=="Отправить релиз",F.chat.type=="private")
async def start_release(message:Message,state:FSMContext):
    await state.clear()
    await state.set_state(FSMStates.single_q1)
    await state.update_data(form_data={},skip_q13=False,skip_q9_q10=False,skip_q12=False,no_gray=False,release_type=None,states_stack=["single_q1"],questions_stack=[])
    text="1. У вас уже есть треки на цифровых площадках VK, Яндекс Музыка, Apple Music, Spotify и тд., или это будет ваш первый релиз?"
    kb=single_q1_kb()
    data=await state.get_data()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q1,F.text.in_(["Уже были релизы","Это первый релиз"]),F.chat.type=="private")
async def single_q1_handler(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q1"]=message.text
    if message.text=="Это первый релиз":data["skip_q13"]=True;data["skip_q12"]=True
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q2");data["states_stack"]=stack
    await state.update_data(**data)
    await state.set_state(FSMStates.single_q2)
    text="2. Что будем выгружать:\n\nСингл, альбом или EP?"
    kb=single_q2_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q2,F.text.in_(["Сингл","Альбом/EP"]),F.chat.type=="private")
async def single_q2_handler(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q2"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q3" if "Сингл" in message.text else "album_q1");data["states_stack"]=stack
    if "Сингл" in message.text:
        data["release_type"]="single"
        await state.set_state(FSMStates.single_q3)
        text="3. ❗ВАЖНАЯ ИНФОРМАЦИЯ❗\n\nДля выгрузки релиза понадобятся:\n\n— Трек в формате WAV 16/24 bit и обложка в размере 1440x1440 или 3000x3000 пикселей в JPG;\n\n— Доказательства на владение битом: пересланные сообщения, скриншоты переписки с фактом оплаты и подтверждением от битмейкера, если бит Free for profit - ссылка на бит. Если сделали сами, то видео проекта из программы;\n\nЕсли захотите отменить выгрузку и вернуться в главное меню - пишите слово «Отмена» в любой момент."
        kb=single_q3_ready_kb()
    else:
        data["release_type"]="album"
        await state.set_state(FSMStates.album_q1)
        text="3. ❗ВАЖНАЯ ИНФОРМАЦИЯ❗\n\nДля выгрузки релиза понадобятся:\n\n— Треки в формате WAV 16/24 bit и обложка в размере 1440x1440 или 3000x3000 пикселей в JPG;\n\n— Доказательства на владение каждым битом: пересланные сообщения, скриншоты переписки с фактом оплаты и подтверждением от битмейкера, если бит Free for profit - ссылка на бит. Если сделали сами, то видео проекта из программы;\n\nЕсли захотите отменить выгрузку и вернуться в главное меню - пишите слово «Отмена» в любой момент."
        kb=single_q3_ready_kb()
    await state.update_data(**data)
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
# ==================== СИНГЛ ====================
@dp.message(FSMStates.single_q3,F.text=="Я готов(-а) выгружать релиз",F.chat.type=="private")
async def single_q3_ready(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q3"]="Готов"
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q4");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q4)
    text="4. Введите название релиза"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
def single_question_handler_factory(state_name:str,question:str,key:str,kb_maker=None):
    async def handler(message:Message,state:FSMContext):
        if message.text=="Отмена":return await reset_to_main_menu(message,state)
        if message.text=="Назад":return await handle_back(message,state)
        await log_user_response(message.from_user.id,message.text)
        data=await state.get_data()
        form=data.get("form_data",{});form[key]=message.text
        data["form_data"]=form
        stack=data.get("states_stack",[]);stack.append(state_name);data["states_stack"]=stack
        await state.update_data(**data);await state.set_state(getattr(FSMStates,state_name))
        kb=kb_maker() if kb_maker else cancel_back_kb()
        qs=data.get("questions_stack",[]);qs.append((question,kb));await state.update_data(questions_stack=qs)
        await send_and_log(message.from_user.id,question,reply_markup=kb)
    return handler
single_q4_handler=single_question_handler_factory("single_q5","5. Введите авторов через запятую (можно использовать feat.)","q4")
single_q5_handler=single_question_handler_factory("single_q6","6. Введите жанр релиза","q5")
single_q6_handler=single_question_handler_factory("single_q7","7. Введите Серую надпись (\"prod. by\", \"Remix\", \"speed up\" и т.д.)\n\nЕсли она не нужна, нажмите пропустить.","q6",kb_maker=skip_only_kb)
dp.message(FSMStates.single_q4)(single_q4_handler)
dp.message(FSMStates.single_q5)(single_q5_handler)
dp.message(FSMStates.single_q6)(single_q6_handler)
@dp.message(FSMStates.single_q7,F.chat.type=="private")
async def single_q7_handler(message:Message,state:FSMContext):
    if message.text=="Отмена":return await reset_to_main_menu(message,state)
    if message.text=="Назад":return await handle_back(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{})
    form["q7"]="Пропущено" if message.text=="Пропустить" else message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q8");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q8)
    text="8. Есть ли в треке вокал? \n\nЕсли он инструментальный, выберите \"Нет\""
    kb=yes_no_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q8,F.text.in_(["Да","Нет"]),F.chat.type=="private")
async def single_q8_handler(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q8"]=message.text
    data["form_data"]=form
    if message.text=="Нет":
        data["skip_q9_q10"]=True
        next_state="single_q11"
        text="11. Введите имя и фамилию авторов текста и музыки, как в паспорте\n\n(Если вокала нет, введите только имя и фамилию композитора)"
        kb=cancel_back_kb()
    else:
        data["skip_q9_q10"]=False
        next_state="single_q9"
        text="9. Есть ли в треке мат, ненормативная или потенциально оскорбительная лексика?"
        kb=yes_no_kb()
    stack=data.get("states_stack",[]);stack.append(next_state);data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(getattr(FSMStates,next_state))
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q9,F.text.in_(["Да","Нет"]),F.chat.type=="private")
async def single_q9_handler(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q9"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q10");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q10)
    text="10. Пришлите текст трека (будет добавлен на Genius)"
    kb=skip_only_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q10,F.chat.type=="private")
async def single_q10_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{})
    form["q10"]="Пропущено" if message.text=="Пропустить" else message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q11");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q11)
    text="11. Введите имя и фамилию авторов текста и музыки, как в паспорте"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q11,F.chat.type=="private")
async def single_q11_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q11"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q12");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q12)
    text="12. Введите дату релиза, минимум за 7 рабочих дней, если хотите отправить релиз на промо, рекомендуем ставить дату релиза не ранее 2-3 недель"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q12,F.chat.type=="private")
async def single_q12_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q12"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q14" if data.get("skip_q13") else "single_q13");data["states_stack"]=stack
    if data.get("skip_q13"):
        await state.update_data(**data);await state.set_state(FSMStates.single_q14)
        text="14. Укажите начало 30-ти секундного отрывка для трека в Tik-Tok / iTunes / Youtube (указывайте в секундах, пожалуйста):\n\nЕсли хотите, чтобы трек включался с самого начала, нажмите «0»"
        kb=zero_kb()
    else:
        await state.update_data(**data);await state.set_state(FSMStates.single_q13)
        text="13. Пришлите ссылки на свои карточки в стриминговых сервисах:\n\n• Карточка в Apple Music;\n• Карточка в Spotify\n\nПример заполнения:\nApple: https://music.apple.com/tr/artist/%D1%81%D0%B5%D1%80%D1%8B%D0%B9%D0%BA%D0%B0%D0%BC%D0%B5%D0%BD%D1%8C/1871720776\nSpotify: https://open.spotify.com/artist/5wJeIrHWcKZ9vl5UTB0WNI"
        kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q13,F.chat.type=="private")
async def single_q13_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q13"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q14");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q14)
    text="14. Укажите начало 30-ти секундного отрывка для трека в Tik-Tok / iTunes / Youtube (указывайте в секундах, пожалуйста):\n\nЕсли хотите, чтобы трек включался с самого начала, нажмите «0»"
    kb=zero_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q14,F.chat.type=="private")
async def single_q14_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q14"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q15");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q15)
    text="15. 🎵 Загрузите файл трека:\n\nПришлите ссылку на Яндекс Диск или Google Drive (откройте для файла общий доступ)\nФормат: wav или flac, 16/24 bit, 44.1khz"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q15,F.chat.type=="private")
async def single_q15_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q15"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q16");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q16)
    text="16. Загрузите обложку:\n\nПришлите ссылку на Яндекс Диск или Google Drive. (Откройте общий доступ).\n\nКвадрат, размер 1440x1440px или 3000x3000px в формате JPG/PNG\n\n❗ВАЖНАЯ ИНФОРМАЦИЯ❗\n\nНадписи должны соответствовать вашим метаданным (ники артистов и название трека) или отсутствовать вовсе. Обложки низкого качества (нечёткие, размытые), с большой вероятностью, не пройдут модерацию и будут отклонены агрегатором. Спасибо за понимание!"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q16,F.chat.type=="private")
async def single_q16_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q16"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q17");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q17)
    text="17. Пришлите доказательства наличия прав на инструментал. Если бит куплен, пришлите договор с битмейкером. Если бит Free For Profit, то пришлите ссылку, по которой вы нашли бит (ролик на YouTube или пост в телеграм канале битмейкера). Если вы сделали бит сами, то пришлите видео из вашей DAW, в котором поочередно включаете дорожки с мелодией, басом и киком"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q17,F.chat.type=="private")
async def single_q17_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q17"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q18");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q18)
    text="18. Хотите получить нотку на свой YouTube канал?\n\n❕ТРЕБОВАНИЯ ВЕРИФИКАЦИИ❕\n\n— Опубликовано хотя бы 1 музыкальное видео\n— Официально выгружен минимум один релиз в системный канал Topic\n— Нет нарушений правил YouTube\n\nЕсли ваш канал соответствует всем требованиям, пришлите в чат ссылку на него"
    kb=skip_only_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q18,F.chat.type=="private")
async def single_q18_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{})
    form["q18"]="Пропущено" if message.text=="Пропустить" else message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q19");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q19)
    text="19. Нужна ли Мультиссылка для релиза (линк с основными площадками)?\n\nВыберите: «Да» или «Нет»\n\nОбразец линка: band.link/6767"
    kb=yes_no_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q19,F.text.in_(["Да","Нет"]),F.chat.type=="private")
async def single_q19_handler(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q19"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q20");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q20)
    text="20. Пришлите ссылки на свои социальные сети артиста:\n\nVK, Telegram, Instagram, YouTube, TikTok"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q20,F.chat.type=="private")
async def single_q20_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q20"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q21");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q21)
    videoshot_text=(
        "21. Загрузите видеошот:\n\n"
        "Пришлите ссылку на Яндекс Диск или Google Drive. (Откройте для неё доступ).\n\n"
        "Технические требования:\n"
        "– видео в формате mp4, H.264\n"
        "– размер 720p (404х720)\n"
        "– длина 15 секунд, не страшно, если будет немного дольше\n"
        "– формат видео желательно вертикальный. Если видео горизонтальное, при вертикальной ориентации экрана мы будем обрезать только центр 405х720 px.\n\n"
        "В качестве видеошотов могут быть использованы:\n"
        "– видео, снятое специально для Яндекс.Музыки;\n"
        "– нарезка из видеоклипа;\n"
        "– кадры из бэкстейджей;\n"
        "– моушндизайн.\n\n"
        "Рекомендации по созданию видеошота:\n"
        "– Лучше не использовать кадры с движением губ (пением): ролик будет зациклен, звук не сможет всегда совпадать с движением губ на видео — это будет раздражать зрителя.\n"
        "– Старайтесь избегать очень коротких кадров — резкие скачки картинки могут смотреться неприятно.\n"
        "– Основные смысловые элементы лучше сосредоточить в центре кадра, чтобы они не обрезались.\n"
        "– Постарайтесь уложить в видеошот короткий законченный сюжет.\n\n"
        "Что не должен содержать видеошот:\n"
        "– текст, не имеющий отношения к треку;\n"
        "– запрещенные вещества, алкоголь, табак, сцены насилия;\n"
        "– рекламу брендов;\n"
        "– рекламу альбома или концерта;\n"
        "– вотермарки сторонних сервисов.\n\n"
    )
    kb=skip_only_kb()
    qs=data.get("questions_stack",[]);qs.append((videoshot_text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,videoshot_text,reply_markup=kb)
@dp.message(FSMStates.single_q21,F.chat.type=="private")
async def single_q21_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{})
    form["q21"]="Пропущено" if message.text=="Пропустить" else message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_q22");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.single_q22)
    text="22. Комментарии по выгрузке для модератора или пожелания:\n\nЕсли его нет, нажмите пропустить."
    kb=skip_only_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.single_q22,F.chat.type=="private")
async def single_q22_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{})
    form["q22"]="Пропущено" if message.text=="Пропустить" else message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("single_confirm");data["states_stack"]=stack
    await state.update_data(**data);await show_single_summary(message,state)
async def show_single_summary(message:Message,state:FSMContext):
    data=await state.get_data();form=data.get("form_data",{})
    skip_q9_q10=data.get("skip_q9_q10",False);skip_q13=data.get("skip_q13",False)
    summary="📋 Анкета релиза (Сингл):\n\n"
    summary+=f"1. {form.get('q1','')}\n2. {form.get('q2','')}\n3. {form.get('q3','')}\n4. Название: {form.get('q4','')}\n5. Авторы: {form.get('q5','')}\n6. Жанр: {form.get('q6','')}\n7. Серая надпись: {form.get('q7','')}\n8. Вокал: {form.get('q8','')}\n"
    if not skip_q9_q10:summary+=f"9. Мат: {form.get('q9','')}\n10. Текст: {form.get('q10','')}\n"
    summary+=f"11. Авторы: {form.get('q11','')}\n12. Дата: {form.get('q12','')}\n"
    if not skip_q13:summary+=f"13. Карточки: {form.get('q13','')}\n"
    summary+=f"14. Отрывок: {form.get('q14','')}\n15. Трек: {form.get('q15','')}\n16. Обложка: {form.get('q16','')}\n17. Права: {form.get('q17','')}\n18. Нотка: {form.get('q18','')}\n19. Мультиссылка: {form.get('q19','')}\n20. Соцсети: {form.get('q20','')}\n21. Видеошот: {form.get('q21','')}\n22. Комментарии: {form.get('q22','')}\n"
    await send_and_log(message.from_user.id,summary)
    await state.set_state(FSMStates.single_confirm)
    stack=data.get("states_stack",[]);stack.append("single_confirm");data["states_stack"]=stack
    await state.update_data(**data)
    text="Проверьте, все ли данные были введены верно"
    kb=confirm_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
# ==================== АЛЬБОМ ====================
@dp.message(FSMStates.album_q1,F.text=="Я готов(-а) выгружать релиз",F.chat.type=="private")
async def album_q1_ready(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q3"]="Готов"
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q2");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q2)
    text="4. Введите свой никнейм (никнеймы через запятую, если авторов релиза несколько, также можно использовать feat.)"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q2,F.chat.type=="private")
async def album_q2_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q4"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q3");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q3)
    text="5. Есть ли в треках вокал? \n\nЕсли альбом инструментальный, то нажимай \"Нет\""
    kb=yes_no_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q3,F.text.in_(["Да","Нет"]),F.chat.type=="private")
async def album_q3_handler(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q5"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q4");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q4)
    text="6. Хотите указать серую надпись?\n\"prod. by\", \"Remix\", \"speed up\" и т.д."
    kb=skip_only_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q4,F.chat.type=="private")
async def album_q4_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{})
    form["q6"]="Пропущено" if message.text=="Пропустить" else message.text
    data["no_gray"]=message.text=="Пропустить"
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q5");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q5)
    q7="7. Выпишите все треки в альбоме по порядку:\n\n1. Исполнитель - Название (есть ли мат, секунда воспроизведения для Тик-Ток)\n2. Исполнитель - Название...\nПример:\n1. автор - крутой трек (мата нет, 28)\n2. автор feat. другой автор - еще один крутой трек (мат есть, 0)\n3. автор ..."
    if not data.get("no_gray"):q7="7. Выпишите все треки в альбоме по порядку:\n\n1. Исполнитель - Название (есть ли мат, prod. by, секунда воспроизведения для Тик-Ток)\n2. Исполнитель - Название...\nПример:\n1. автор - крутой трек (мата нет, clean version, 28)\n2. автор feat. другой автор - еще один крутой трек (мат есть, prod. by #серыйкамень, 0)\n3. автор ..."
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((q7,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,q7,reply_markup=kb)
@dp.message(FSMStates.album_q5,F.chat.type=="private")
async def album_q5_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q7"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q6");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q6)
    text="8. Введите жанр релиза"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q6,F.chat.type=="private")
async def album_q6_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q8"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q7");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q7)
    q9="9. Введите ФИО артистов из каждого трека, а также укажите авторов минуса и текста по образцу:\n\n📎 Образец заполнения:\n\n1. автор - крутой трек\nИнструментал: Фамилия Имя Отчество\nАвтор слов: Фамилия Имя Отчество\n2. автор feat. другой автор - еще один крутой трек\nИнструментал: Фамилия Имя Отчество, Фамилия другого автора Имя другого автора Отчество другого автора\nАвтор слов: Фамилия Имя Отчество\n3. автор ..."
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((q9,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,q9,reply_markup=kb)
@dp.message(FSMStates.album_q7,F.chat.type=="private")
async def album_q7_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q9"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q8");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q8)
    text="10. Пришлите текст каждого трека (будет добавлен на Genius)"
    kb=skip_only_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q8,F.chat.type=="private")
async def album_q8_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{})
    form["q10"]="Пропущено" if message.text=="Пропустить" else message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q9");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q9)
    text="11. Введите дату релиза, минимум за 7 рабочих дней, если хотите отправить релиз на промо, рекомендуем ставить дату релиза не ранее 2-3 недель"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q9,F.chat.type=="private")
async def album_q9_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q11"]=message.text
    data["form_data"]=form
    skip=data.get("skip_q12",False)
    stack=data.get("states_stack",[]);stack.append("album_q11" if skip else "album_q10");data["states_stack"]=stack
    if skip:
        await state.update_data(**data);await state.set_state(FSMStates.album_q11)
        text="13. 🎵 Загрузите файлы треков:\n\nПришлите одну ссылку на все треки в папке на Яндекс Диск или Google Drive (откройте для папки общий доступ).\n\n❗ВАЖНАЯ ИНФОРМАЦИЯ❗\n\nВсе треки должны быть в одной папке и доступны к прослушиванию без предварительного скачивания.\nФормат: wav или flac, 16/24 bit, 44.1khz."
        kb=cancel_back_kb()
    else:
        await state.update_data(**data);await state.set_state(FSMStates.album_q10)
        text="12. Пришлите ссылки на карточки всех исполнителей в стриминговых сервисах:\n\n• Карточка в Apple Music;\n• Карточка в Spotify\n\nПример заполнения (если автором всех треков в релизе являетесь вы один):\nApple: https://music.apple.com/tr/artist/%D1%81%D0%B5%D1%80%D1%8B%D0%B9%D0%BA%D0%B0%D0%BC%D0%B5%D0%BD%D1%8C/1871720776\nSpotify: https://open.spotify.com/artist/5wJeIrHWcKZ9vl5UTB0WNI"
        kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q10,F.chat.type=="private")
async def album_q10_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q12"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q11");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q11)
    text="13. 🎵 Загрузите файлы треков:\n\nПришлите одну ссылку на все треки в папке на Яндекс Диск или Google Drive (откройте для папки общий доступ).\n\n❗ВАЖНАЯ ИНФОРМАЦИЯ❗\n\nВсе треки должны быть в одной папке и доступны к прослушиванию без предварительного скачивания.\nФормат: wav или flac, 16/24 bit, 44.1khz."
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q11,F.chat.type=="private")
async def album_q11_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q13"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q12");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q12)
    text="14. Загрузите обложку:\n\nПришлите ссылку на Яндекс Диск или Google Drive. (Откройте общий доступ).\n\nКвадрат, размер 1440x1440px или 3000x3000px в формате JPG/PNG\n\n❗ВАЖНАЯ ИНФОРМАЦИЯ❗\n\nНадписи должны соответствовать вашим метаданным (ники артистов и название трека) или отсутствовать вовсе. Обложки низкого качества (нечёткие, размытые), с большой вероятностью, не пройдут модерацию и будут отклонены агрегатором. Спасибо за понимание!"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q12,F.chat.type=="private")
async def album_q12_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q14"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q13");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q13)
    text="15. Пришлите доказательства наличия прав на инструментал (у всех треков). Если бит куплен, пришлите договор с битмейкером. Если бит Free For Profit, то пришлите ссылку, по которой вы нашли бит (ролик на YouTube или пост в телеграм канале битмейкера). Если вы сделали бит сами, то пришлите видео из вашей DAW, в котором поочередно включаете дорожки с мелодией, басом и киком. Все доказательства загрузите на Яндекс Диск или Google Drive, если у вас такой возможности нет, то пришлите доказательства агенту поддержки: @devo4kawlekarstvo, а здесь напишите: \"прислал в личные сообщения поддержке\""
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q13,F.chat.type=="private")
async def album_q13_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q15"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q14");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q14)
    text="16. Хотите получить нотку на свой YouTube канал?\n\n❕ТРЕБОВАНИЯ ВЕРИФИКАЦИИ❕\n\n— Опубликовано хотя бы 1 музыкальное видео\n— Официально выгружен минимум один релиз в системный канал Topic\n— Нет нарушений правил YouTube\n\nЕсли ваш канал соответствует всем требованиям, пришлите в чат ссылку на него"
    kb=skip_only_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q14,F.chat.type=="private")
async def album_q14_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{})
    form["q16"]="Пропущено" if message.text=="Пропустить" else message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q15");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q15)
    text="17. Нужна ли Мультиссылка для релиза (линк с основными площадками)?\n\nВыберите: «Да» или «Нет»\n\nОбразец линка: band.link/6767"
    kb=yes_no_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q15,F.text.in_(["Да","Нет"]),F.chat.type=="private")
async def album_q15_handler(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q17"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q16");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q16)
    text="18. Пришлите ссылки на свои социальные сети артиста:\n\nVK, Telegram, Instagram, YouTube, TikTok"
    kb=cancel_back_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q16,F.chat.type=="private")
async def album_q16_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{});form["q18"]=message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q17");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q17)
    videoshot_text=(
        "19. Загрузите видеошоты:\n\n"
        "Пришлите ссылку на Яндекс Диск или Google Drive. (Откройте для неё доступ).\n\n"
        "Технические требования:\n"
        "– видео в формате mp4, H.264\n"
        "– размер 720p (404х720)\n"
        "– длина 15 секунд, не страшно, если будет немного дольше\n"
        "– формат видео желательно вертикальный. Если видео горизонтальное, при вертикальной ориентации экрана мы будем обрезать только центр 405х720 px.\n\n"
        "В качестве видеошотов могут быть использованы:\n"
        "– видео, снятое специально для Яндекс.Музыки;\n"
        "– нарезка из видеоклипа;\n"
        "– кадры из бэкстейджей;\n"
        "– моушндизайн.\n\n"
        "Рекомендации по созданию видеошота:\n"
        "– Лучше не использовать кадры с движением губ (пением): ролик будет зациклен, звук не сможет всегда совпадать с движением губ на видео — это будет раздражать зрителя.\n"
        "– Старайтесь избегать очень коротких кадров — резкие скачки картинки могут смотреться неприятно.\n"
        "– Основные смысловые элементы лучше сосредоточить в центре кадра, чтобы они не обрезались.\n"
        "– Постарайтесь уложить в видеошот короткий законченный сюжет.\n\n"
        "Что не должен содержать видеошот:\n"
        "– текст, не имеющий отношения к треку;\n"
        "– запрещенные вещества, алкоголь, табак, сцены насилия;\n"
        "– рекламу брендов;\n"
        "– рекламу альбома или концерта;\n"
        "– вотермарки сторонних сервисов.\n\n"
    )
    kb=skip_only_kb()
    qs=data.get("questions_stack",[]);qs.append((videoshot_text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,videoshot_text,reply_markup=kb)
@dp.message(FSMStates.album_q17,F.chat.type=="private")
async def album_q17_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{})
    form["q19"]="Пропущено" if message.text=="Пропустить" else message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_q18");data["states_stack"]=stack
    await state.update_data(**data);await state.set_state(FSMStates.album_q18)
    text="20. Комментарии по выгрузке для модератора или пожелания:\n\nЕсли его нет, нажмите пропустить."
    kb=skip_only_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
@dp.message(FSMStates.album_q18,F.chat.type=="private")
async def album_q18_handler(message:Message,state:FSMContext):
    if message.text in ["Отмена","Назад"]:return await handle_back_cancel_unified(message,state)
    await log_user_response(message.from_user.id,message.text)
    data=await state.get_data()
    form=data.get("form_data",{})
    form["q20"]="Пропущено" if message.text=="Пропустить" else message.text
    data["form_data"]=form
    stack=data.get("states_stack",[]);stack.append("album_confirm");data["states_stack"]=stack
    await state.update_data(**data);await show_album_summary(message,state)
async def show_album_summary(message:Message,state:FSMContext):
    data=await state.get_data();form=data.get("form_data",{})
    skip_q12=data.get("skip_q12",False)
    summary="📋 Анкета релиза (Альбом/EP):\n\n"
    summary+=f"1. {form.get('q1','')}\n2. {form.get('q2','')}\n3. {form.get('q3','')}\n4. Никнейм: {form.get('q4','')}\n5. Вокал: {form.get('q5','')}\n6. Серая надпись: {form.get('q6','')}\n7. Треки: {form.get('q7','')}\n8. Жанр: {form.get('q8','')}\n9. ФИО: {form.get('q9','')}\n10. Тексты: {form.get('q10','')}\n11. Дата: {form.get('q11','')}\n"
    if not skip_q12:summary+=f"12. Карточки: {form.get('q12','')}\n"
    summary+=f"13. Файлы треков: {form.get('q13','')}\n14. Обложка: {form.get('q14','')}\n15. Права: {form.get('q15','')}\n16. Нотка: {form.get('q16','')}\n17. Мультиссылка: {form.get('q17','')}\n18. Соцсети: {form.get('q18','')}\n19. Видеошоты: {form.get('q19','')}\n20. Комментарии: {form.get('q20','')}\n"
    await send_and_log(message.from_user.id,summary)
    await state.set_state(FSMStates.album_confirm)
    stack=data.get("states_stack",[]);stack.append("album_confirm");data["states_stack"]=stack
    await state.update_data(**data)
    text="Проверьте, все ли данные были введены верно"
    kb=confirm_kb()
    qs=data.get("questions_stack",[]);qs.append((text,kb));await state.update_data(questions_stack=qs)
    await send_and_log(message.from_user.id,text,reply_markup=kb)
# ==================== ОБРАБОТЧИКИ НАЗАД/ОТМЕНА ====================
async def handle_back(message:Message,state:FSMContext):
    data=await state.get_data()
    stack=data.get("states_stack",[])
    if len(stack)<2:
        await send_and_log(message.from_user.id,"Нельзя вернуться назад.",reply_markup=cancel_back_kb())
        return
    stack.pop()
    prev_state=stack[-1]
    form=data.get("form_data",{})
    last_q=max([k for k in form.keys() if k.startswith('q')],default=None)
    if last_q:del form[last_q]
    qs=data.get("questions_stack",[])
    if len(qs)>=1:
        qs.pop()
        prev_text,prev_kb=qs[-1]
    else:
        prev_text,prev_kb="",None
    data["form_data"]=form;data["states_stack"]=stack;data["questions_stack"]=qs
    await state.update_data(**data);await state.set_state(getattr(FSMStates,prev_state))
    await send_and_log(message.from_user.id,prev_text,reply_markup=prev_kb)
async def handle_back_cancel_unified(message:Message,state:FSMContext):
    if message.text=="Отмена":await reset_to_main_menu(message,state)
    elif message.text=="Назад":await handle_back(message,state)
@dp.message(F.text=="Отмена",F.chat.type=="private")
async def cancel_global(message:Message,state:FSMContext):
    await reset_to_main_menu(message,state)
@dp.message(F.text=="Назад",F.chat.type=="private")
async def back_global(message:Message,state:FSMContext):
    await handle_back(message,state)
# ==================== ОТПРАВКА НА МОДЕРАЦИЮ ====================
@dp.message(FSMStates.single_confirm,F.text=="Отправить на модерацию",F.chat.type=="private")
async def send_single_to_moderation(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    user_id=message.from_user.id
    data=await state.get_data();form=data.get("form_data",{})
    skip_q9_q10=data.get("skip_q9_q10",False);skip_q13=data.get("skip_q13",False)
    summary="📋 Анкета релиза (Сингл):\n\n"
    summary+=f"1. {form.get('q1','')}\n2. {form.get('q2','')}\n3. {form.get('q3','')}\n4. Название: {form.get('q4','')}\n5. Авторы: {form.get('q5','')}\n6. Жанр: {form.get('q6','')}\n7. Серая надпись: {form.get('q7','')}\n8. Вокал: {form.get('q8','')}\n"
    if not skip_q9_q10:summary+=f"9. Мат: {form.get('q9','')}\n10. Текст: {form.get('q10','')}\n"
    summary+=f"11. Авторы: {form.get('q11','')}\n12. Дата: {form.get('q12','')}\n"
    if not skip_q13:summary+=f"13. Карточки: {form.get('q13','')}\n"
    summary+=f"14. Отрывок: {form.get('q14','')}\n15. Трек: {form.get('q15','')}\n16. Обложка: {form.get('q16','')}\n17. Права: {form.get('q17','')}\n18. Нотка: {form.get('q18','')}\n19. Мультиссылка: {form.get('q19','')}\n20. Соцсети: {form.get('q20','')}\n21. Видеошот: {form.get('q21','')}\n22. Комментарии: {form.get('q22','')}\n"
    await bot.send_message(GROUP_ID,"@clockerka",message_thread_id=MODERATION_TOPIC_ID)
    await bot.send_message(GROUP_ID,summary,message_thread_id=MODERATION_TOPIC_ID,reply_markup=mod_actions_kb(user_id))
    await send_and_log(user_id,"Анкета отправлена модератору.",reply_markup=main_menu_kb())
    await state.clear()
@dp.message(FSMStates.album_confirm,F.text=="Отправить на модерацию",F.chat.type=="private")
async def send_album_to_moderation(message:Message,state:FSMContext):
    await log_user_response(message.from_user.id,message.text)
    user_id=message.from_user.id
    data=await state.get_data();form=data.get("form_data",{})
    skip_q12=data.get("skip_q12",False)
    summary="📋 Анкета релиза (Альбом/EP):\n\n"
    summary+=f"1. {form.get('q1','')}\n2. {form.get('q2','')}\n3. {form.get('q3','')}\n4. Никнейм: {form.get('q4','')}\n5. Вокал: {form.get('q5','')}\n6. Серая надпись: {form.get('q6','')}\n7. Треки: {form.get('q7','')}\n8. Жанр: {form.get('q8','')}\n9. ФИО: {form.get('q9','')}\n10. Тексты: {form.get('q10','')}\n11. Дата: {form.get('q11','')}\n"
    if not skip_q12:summary+=f"12. Карточки: {form.get('q12','')}\n"
    summary+=f"13. Файлы треков: {form.get('q13','')}\n14. Обложка: {form.get('q14','')}\n15. Права: {form.get('q15','')}\n16. Нотка: {form.get('q16','')}\n17. Мультиссылка: {form.get('q17','')}\n18. Соцсети: {form.get('q18','')}\n19. Видеошоты: {form.get('q19','')}\n20. Комментарии: {form.get('q20','')}\n"
    await bot.send_message(GROUP_ID,"@clockerka",message_thread_id=MODERATION_TOPIC_ID)
    await bot.send_message(GROUP_ID,summary,message_thread_id=MODERATION_TOPIC_ID,reply_markup=mod_actions_kb(user_id))
    await send_and_log(user_id,"Анкета отправлена модератору.",reply_markup=main_menu_kb())
    await state.clear()
# ==================== МОДЕРАЦИЯ ====================
@dp.callback_query(F.data.startswith("mod_approve:"))
async def mod_approve(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    user_id=int(callback.data.split(":")[1])
    await send_and_log(user_id,"Релиз был одобрен модератором, и после обработки агрегатором мы пришлем вам UPC код релиза")
    await callback.answer()
@dp.callback_query(F.data.startswith("mod_reject:"))
async def mod_reject(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(FSMStates.mod_reject_reason)
    await state.update_data(mod_message_id=callback.message.message_id,mod_chat_id=callback.message.chat.id,mod_thread_id=callback.message.message_thread_id)
    await callback.message.answer("Введите причину отказа:")
    await callback.answer()
@dp.message(FSMStates.mod_reject_reason)
async def mod_reject_reason(message:Message,state:FSMContext):
    data=await state.get_data()
    reason=message.text
    await bot.send_message(data['mod_chat_id'],f"Релиз отклонен. Причина: {reason}",message_thread_id=data['mod_thread_id'])
    await message.answer("Причина отказа отправлена.")
    await state.clear()
# ==================== ПЕРЕСЫЛКА СООБЩЕНИЙ ====================
@dp.message(F.chat.type=="private")
async def private_msg(message:Message,state:FSMContext):
    if await state.get_state():return
    user_id=message.from_user.id
    username=message.from_user.username
    if user_id not in user_topics:
        topic_name=f"{user_id} ({username})" if username else str(user_id)
        try:
            topic=await bot.create_forum_topic(GROUP_ID,name=topic_name)
            user_topics[user_id]=topic.message_thread_id
            topic_to_user[topic.message_thread_id]=user_id
        except Exception as e:
            await send_and_log(user_id,f"Ошибка при создании темы: {e}")
            return
    display_name=f"@{username}" if username else message.from_user.full_name
    try:
        if message.text:
            await bot.send_message(GROUP_ID,f"{message.text}\n\n\n{display_name}",message_thread_id=user_topics[user_id],disable_notification=True)
        elif message.caption:
            await bot.send_message(GROUP_ID,f"{message.caption}\n\n\n{display_name}",message_thread_id=user_topics[user_id],disable_notification=True)
        elif message.photo:
            await bot.send_photo(GROUP_ID,message.photo[-1].file_id,caption=f"{message.caption or ''}\n\n\n{display_name}",message_thread_id=user_topics[user_id],disable_notification=True)
        elif message.video:
            await bot.send_video(GROUP_ID,message.video.file_id,caption=f"{message.caption or ''}\n\n\n{display_name}",message_thread_id=user_topics[user_id],disable_notification=True)
        elif message.document:
            await bot.send_document(GROUP_ID,message.document.file_id,caption=f"{message.caption or ''}\n\n\n{display_name}",message_thread_id=user_topics[user_id],disable_notification=True)
        elif message.audio:
            await bot.send_audio(GROUP_ID,message.audio.file_id,caption=f"{message.caption or ''}\n\n\n{display_name}",message_thread_id=user_topics[user_id],disable_notification=True)
        elif message.voice:
            await bot.send_voice(GROUP_ID,message.voice.file_id,caption=f"{message.caption or ''}\n\n\n{display_name}",message_thread_id=user_topics[user_id],disable_notification=True)
        else:
            await bot.send_message(GROUP_ID,f"<{display_name} отправил неподдерживаемый тип сообщения>",message_thread_id=user_topics[user_id],disable_notification=True)
    except Exception as e:
        await send_and_log(user_id,f"Ошибка при отправке в тему: {e}")
@dp.message(F.chat.type=="supergroup",F.message_thread_id.is_not(None))
async def group_msg(message:Message):
    if message.chat.id!=GROUP_ID or message.from_user.id==bot.id:return
    thread_id=message.message_thread_id
    if thread_id in topic_to_user:
        user_id=topic_to_user[thread_id]
        if message.text:
            await bot.send_message(user_id,f"сообщение от администратора: {message.text}")
        elif message.caption:
            await bot.send_message(user_id,f"сообщение от администратора: {message.caption}")
        else:
            await bot.send_message(user_id,f"сообщение от администратора: [Медиа]")
async def main():
    await dp.start_polling(bot)
if __name__=="__main__":
    asyncio.run(main())