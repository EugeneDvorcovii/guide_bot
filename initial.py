from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data_clients.MySQLClient import DataClient
from languages.languages import  languages

from config import MAIN_TOKEN


data_client = DataClient()
data_client.create_db()

"""
AgACAgIAAxkBAAIO_2XgoY-fHE7mQ4SjzEJm59XooLsLAALT1zEbyMYAAUuOiUQ1x3xrvwEAAwIAA3kAAzQE

"""
# print(data_client.get_random_ask(quiz_id=14, ask_id_ready=[37, 38]))
# data_client.set_new_quiz_theme(title="Geographic",
#                                description="The quizzes are dedicated to the knowledge of the geography of Russia.",
#                                language="en")
# data_client.set_new_quiz(theme_id=23,
#                          title="Natural attractions",
#                          description="The questions are devoted to the natural attractions of Russia")
# data_client.set_new_quiz_ask(quiz_id=19,
#                              quiz_ask="The famous Lena Pillars rise as formidable cliffs on the rocks of one of the major rivers of Yakutia. What river are they on?",
#                              t_q="Lena River",
#                              f_q1="Indigirka River",
#                              f_q2="Kolyma River",
#                              f_q3="Olenek River",
#                              image_id="AgACAgIAAxkBAAIO_2XgoY-fHE7mQ4SjzEJm59XooLsLAALT1zEbyMYAAUuOiUQ1x3xrvwEAAwIAA3kAAzQE")
# data_client.set_new_quiz_ask(quiz_id=19,
#                              quiz_ask="The Curonian Spit, which is partly Russian territory, has many amazing natural attractions. Which of natural attraction is not at The Curonian Spit?",
#                              t_q="Weathering pillars",
#                              f_q1="Dancing Forest",
#                              f_q2="Huge sand dunes",
#                              f_q3="Lake «Swan»",
#                              image_id="AgACAgIAAxkBAAIPAWXgoae5rpdtomDIpXWp7RJit9KmAALb1zEbyMYAAUtuZ0czEN6mVAEAAwIAA3kAAzQE")
# data_client.set_new_quiz_ask(quiz_id=19,
#                              quiz_ask="Probably everyone knows about the deepest lake on the planet. Lake Baikal is not only the deepest but also one of the most beautiful. The only river that flows from this lake is...",
#                              t_q="Angara River",
#                              f_q1="Irtysh River",
#                              f_q2="Lena River",
#                              f_q3="Indigirka River",
#                              image_id="AgACAgIAAxkBAAIPA2Xgoa_cqNwgaxG9jDhQeW7joJ0FAALc1zEbyMYAAUv3OvNtkwtO0gEAAwIAA3kAAzQE")
# data_client.set_new_quiz_ask(quiz_id=19,
#                              quiz_ask="This natural attraction located on the Man-Pupu-Ner plateau can confidently be called the landmark of the Urals. Have you guessed what this is about?",
#                              t_q="Weathering pillars",
#                              f_q1="Lena Pillars ",
#                              f_q2="Stolbichi",
#                              f_q3="The Rocky Mountains",
#                              image_id="AgACAgIAAxkBAAIPBWXgobaqzAc6yDBdFhyrhXmpZN6KAALe1zEbyMYAAUsMDqvx0l_6ZQEAAwIAA3kAAzQE")
# data_client.set_new_quiz_ask(quiz_id=19,
#                              quiz_ask="This volcano is the largest as well as the most active in Kamchatka region. Can you guess it? Klyuchevskaya Sopka",
#                              t_q="Klyuchevskaya Sopka",
#                              f_q1="Tyatya",
#                              f_q2="Avachinskaya Sopka   ",
#                              f_q3="Vesuvius",
#                              image_id="AgACAgIAAxkBAAIPB2Xgob6S0Nlpl1nVsRWRp8Q-hst8AALg1zEbyMYAAUs89lM2ZtPrNgEAAwIAA3kAAzQE")
# data_client.set_new_quiz_ask(quiz_id=19,
#                              quiz_ask="There is the place called “Fiery Eagle’s Nest” among the local population.  This mysterious object located in the Irkutsk region was discovered in 1949. Do you know what this is?",
#                              t_q="Patomskiy crater",
#                              f_q1="Kolyma Upland",
#                              f_q2="Yablonovy Mountains",
#                              f_q3="Kodar Mountains",
#                              image_id="AgACAgIAAxkBAAIPCWXgocNd4H-Su9g31jfYJXDAEOO5AALi1zEbyMYAAUtP8Cd7CSWKcwEAAwIAA3kAAzQE")
# data_client.set_new_quiz_ask(quiz_id=19,
#                              quiz_ask="The only geyser field in Russia and Eurasia, one of the largest such places in the world. On its surface there are about 20 large geysers and many hot springs that emit water or steam. Where is it located?",
#                              t_q="Kamchatka Region",
#                              f_q1="Taymyr Peninsula",
#                              f_q2="Putorana Plateau",
#                              f_q3="Kodar Mountains",
#                              image_id="AgACAgIAAxkBAAIPC2XgocdbTLJUJv7UsOaEK_sl1xBkAALj1zEbyMYAAUtHaJFI87Rx5wEAAwIAA3kAAzQE")
storage = MemoryStorage()

bot = Bot(token=MAIN_TOKEN)
dp = Dispatcher(bot, storage=storage)