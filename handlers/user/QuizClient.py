from aiogram import types
from initial import bot, dp
from keyboards import create_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from random import shuffle

from initial import DataClient


# from handlers.user.choice_place import
from config import FSMWorkProgram
# from handlers.user.choice_place_base import ChoicePlaceBase


class QuizClient:
    quiz_menu_btn = ["Статистика", "Играть"]

    def __init__(self, data_client: DataClient):
        self.data_client = data_client

    async def user_quiz_menu(self, msg: types.Message):
        await msg.answer("Выберите дальнейшее действие.",
                         reply_markup=create_keyboards(self.quiz_menu_btn, cancel_btn=True))
        await FSMWorkProgram.user_quiz_menu.set()

    async def get_statistic(self, msg: types.Message):
        user_id = self.data_client.get_user_id(msg.from_user.id)
        data = self.data_client.get_statistics(user_id=user_id)
        await msg.answer(data)

    async def get_quiz_theme(self, msg: types.Message):
        btn = self.data_client.get_quiz_theme_list()[1]
        await msg.answer("Выберите тему квиза.",
                         reply_markup=create_keyboards(btn, cancel_btn=True))
        await FSMWorkProgram.get_quiz_theme.set()

    async def get_quiz(self, msg: types.Message, state: FSMContext):
        quiz_theme_id = self.data_client.get_quiz_theme_id(msg.text)
        async with state.proxy() as data:
            data["quiz_theme_id"] = quiz_theme_id
            data["quiz_theme_title"] = msg.text
        btn = self.data_client.get_quiz_list(quiz_theme_id)[1]
        await msg.answer("Выберите квиз.",
                         reply_markup=create_keyboards(btn, cancel_btn=True))
        await FSMWorkProgram.get_quiz.set()

    async def run_quiz(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            quiz_id = self.data_client.get_quiz_id(msg.text)
            data["quiz_id"] = quiz_id
            data["quiz_title"] = msg.text
            quiz_ask = self.data_client.get_quiz_ask(quiz_id=data["quiz_id"], ask_id=list())
            if quiz_ask[0]:
                quiz_ask = quiz_ask[1]
                ask = quiz_ask["ask"]
                answers = [quiz_ask["t_q"], quiz_ask["f_q1"], quiz_ask["f_q2"], quiz_ask["f_q3"]]
                shuffle(answers)
                image_id = quiz_ask["image_id"]
                data["true_q"] = quiz_ask["t_q"]
                data["ask_id"] = [quiz_ask["id"]]
                data["user_id"] = self.data_client.get_user_id(msg.from_user.id)
                await msg.answer_photo(image_id, ask,
                                       reply_markup=create_keyboards(answers, cancel_btn=True))
                await FSMWorkProgram.run_quiz.set()
            else:
                await msg.answer("Вы уже ответили на все вопросы.",
                                 reply_markup=create_keyboards(list(), cancel_btn=True))

    async def quiz(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if data["true_q"] == msg.text:
                await msg.answer("Правильный ответ!")
                score = 10
            else:
                await msg.answer(f"Ошибка. Правильный ответ: {data['true_q']}.")
                score = 0
            self.data_client.set_score_user_quiz(user_id=data["user_id"], quiz_id=data["quiz_id"], score=score)
            quiz_ask = self.data_client.get_quiz_ask(quiz_id=data["quiz_id"], ask_id=data["ask_id"])
            if quiz_ask[0]:
                quiz_ask = quiz_ask[1]
                ask = quiz_ask["ask"]
                answers = [quiz_ask["t_q"], quiz_ask["f_q1"], quiz_ask["f_q2"], quiz_ask["f_q3"]]
                shuffle(answers)
                image_id = quiz_ask["image_id"]
                data["true_q"] = quiz_ask["t_q"]
                data["ask_id"].append(quiz_ask["id"])
                print(data["ask_id"])
                await msg.answer_photo(image_id, ask,
                                       reply_markup=create_keyboards(answers, cancel_btn=True))
            else:
                await msg.answer("Вы уже ответили на все вопросы.",
                                 reply_markup=create_keyboards(list(), cancel_btn=True))

    def run_handler(self) -> None:
        dp.register_message_handler(self.user_quiz_menu,
                                    Text(equals="Викторины", ignore_case=True),
                                    state=FSMWorkProgram.main_menu)

        dp.register_message_handler(self.get_statistic,
                                    Text(equals="Статистика", ignore_case=True),
                                    state=FSMWorkProgram.user_quiz_menu)

        dp.register_message_handler(self.get_quiz_theme,
                                    Text(equals="Играть", ignore_case=True),
                                    state=FSMWorkProgram.user_quiz_menu)
        dp.register_message_handler(self.get_quiz,
                                    state=FSMWorkProgram.get_quiz_theme)
        dp.register_message_handler(self.run_quiz,
                                    state=FSMWorkProgram.get_quiz)
        dp.register_message_handler(self.quiz,
                                    state=FSMWorkProgram.run_quiz)




