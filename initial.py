from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data_clients.MySQLClient import DataClient

from config import MAIN_TOKEN


data_client = DataClient()
data_client.create_db()
data_client.set_new_quiz_theme(title="Россия",
                               description="Квизы посвящены знанию нашей Родины.")
data_client.set_new_quiz(theme_id=1,
                         title="Факты про Россию, часть 1",
                         description="В этом квизе будут вопросы по России.")
data_client.set_new_quiz_ask(quiz_id=1,
                             quiz_ask="Какая площадь России?",
                             t_q="17млн",
                             f_q1="15млн",
                             f_q2="14млн",
                             f_q3="13млн",
                             image_id="AgACAgIAAxkBAAIJg2XWCTMS7ML-ic9_Htrpo-gx2SfYAAKi2jEb21iwSv1NZbzeRvoLAQADAgADeQADNAQ")
data_client.set_new_quiz_ask(quiz_id=1,
                             quiz_ask="Как называется извергающийся вулкан в России?",
                             t_q="Ключевская Сопка",
                             f_q1="Этна",
                             f_q2="Визувий",
                             f_q3="Котопахи",
                             image_id="AgACAgIAAxkBAAIJg2XWCTMS7ML-ic9_Htrpo-gx2SfYAAKi2jEb21iwSv1NZbzeRvoLAQADAgADeQADNAQ")
data_client.set_new_quiz_ask(quiz_id=1,
                             quiz_ask="Где находилась столица России с 1712 по 1918 год?",
                             t_q="Санкт-Петербург",
                             f_q1="Москва",
                             f_q2="Сибирь",
                             f_q3="Краснодар",
                             image_id="AgACAgIAAxkBAAIJg2XWCTMS7ML-ic9_Htrpo-gx2SfYAAKi2jEb21iwSv1NZbzeRvoLAQADAgADeQADNAQ")
storage = MemoryStorage()

bot = Bot(token=MAIN_TOKEN)
dp = Dispatcher(bot, storage=storage)