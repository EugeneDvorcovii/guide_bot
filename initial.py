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
# data_client.set_new_quiz_theme(title="География",
#                                description="Викторины посвящены знанию географии России.",
#                                language="ru")
# data_client.set_new_quiz(theme_id=24,
#                          title="Россия или нет?",
#                          description="Угадайте, изображена на снимке Россия или другая страна")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? I",
#                              t_q="Да это же Байкал! Не обманете.",
#                              f_q1="Очень похоже на североамериканские Великие озера.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP32Xg7jJBWInA78RYkBcp3RNJj8YkAAJS2TEb148JSzyaeBHtacSUAQADAgADeAADNAQ",
#                              big_answer="Разумеется, это Байкал﻿ — самое древнее и самое глубокое озеро планеты. Если воду Байкала поделить между всеми жителями России, то каждому из нас ее запаса хватит на целых 170 тысяч лет.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? II",
#                              t_q="Видимо, на фото — радужные горы в Перу.",
#                              f_q1="Это Хибины — горный массив на Кольском полуострове.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP4WXg7m-ssPYo7rAg9x_RsZVLOsyIAAJT2TEb148JS8CMZrDt_pUiAQADAgADeAADNAQ",
#                              big_answer="Необычные цветные слои гор Виникунка образованы из красного песчаника, который за много миллионов лет под воздействием климата и подземных вод окрасился в самые разные тона.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? III",
#                              t_q="Как много соли… Должно быть, это российское озеро Баскунчак.",
#                              f_q1="Так это же Мертвое море, его сложно с чем-то спутать.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP42Xg7txlHVPdygUAAUn4py5e6pdDnQACVNkxG9ePCUu8tepo-llooAEAAwIAA3gAAzQE",
#                              big_answer="На фото запечатлен Баскунчак﻿ — одно из самых насыщенных солью озер в мире. Здесь добывают 80% отечественной соли, запасов которой хватит еще на 4000 лет.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? IV",
#                              t_q="Это Ключевская Сопка, знаменитый камчатский вулкан.",
#                              f_q1="Это гора Фудзияма: на всех фото из соцсетей она именно так выглядит.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP5WXg7wYuE490saCWGYpclXvVG0ipAAJX2TEb148JS3HIpmh9perRAQADAgADeAADNAQ",
#                              big_answer="Ключевская Сопка — самый высокий действующий вулкан Евразии. Его высота составляет целых 4750 метров над уровнем моря.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? V",
#                              t_q="Разумеется, это знаменитый Прованс.",
#                              f_q1="Родные лавандовые поля в Крыму.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP52Xg7y3LiYstDwKKpGXEXholsfjHAAJY2TEb148JS1N09HfFZ9XTAQADAgADeAADNAQ",
#                              big_answer="Активнее всего лаванда цветет в период с середины июня по середину августа. А лучшим временем для поездки на знаменитые прованские поля эксперты по туризму считают последнюю неделю июня и июль.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? VI",
#                              t_q="Фото сделано на Алтае — это долина реки Чулышман.",
#                              f_q1="Это знаменитая азиатская река Брахмапутра — узнаю колоритный рельеф.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP6WXg71uHubSfyz2FWEnDF_a-5qCcAAJZ2TEb148JS5Rplq9UXGRtAQADAgADeAADNAQ",
#                              big_answer="На фото — Чулышман, одна из крупнейших рек Горного Алтая﻿. Ее нрав весьма крут: течение Чулышман сильное, быстрое, в нем есть множество порогов, водопадов и перекатов.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? VII",
#                              t_q="Кажется, это Шоколадные холмы на Филиппинах.",
#                              f_q1="Однозначно Бэровские бугры в Прикаспийской низменности.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP62Xg756U0hA5Rg7uM2TIjT_qhx0zAAJj2TEb148JS8oAAWeCvwga9AEAAwIAA3gAAzQE",
#                              big_answer="Аппетитное название эти холмы получили из-за того, что в сухой сезон покрывающая их трава меняет цвет с зеленого на шоколадный.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? VIII",
#                              t_q="Конечно, это норвежские фьорды.",
#                              f_q1="Это крутые берега реки Лены.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP7WXg79MkG5Q9vHXy0_R2ygKyXVuuAAJn2TEb148JSwVV_vbjHrWLAQADAgADeAADNAQ",
#                              big_answer="Гейрангер-фьорд включен в Список всемирного наследия ЮНЕСКО, а в поселке, который располагается неподалеку, работает Музей фьордов, посвященный истории и природе региона.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? IX",
#                              t_q="Думаю, это плато Путорана.",
#                              f_q1="Какой интересный снимок Гранд-Каньона в Аризоне.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP72Xg7_YB1eiPv-2rJc_pd6tQcrToAAJp2TEb148JSwRrGimBKI_PAQADAgADeAADNAQ",
#                              big_answer="Плато Путорана﻿ — один из самых малоизученных районов нашей страны. На его территории, площадь которой превышает некоторые страны, например Великобританию, находится около 25 тысяч озер — и нет ни одного населенного пункта.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? X",
#                              t_q="На фото — термальные источники Памуккале в Турции.",
#                              f_q1="Это курорт Мацеста в городе Сочи.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP8WXg8BvPXYn8e_SPOvNNXYnIJWytAAJq2TEb148JS8lpE0t8pwetAQADAgADeAADNAQ",
#                              big_answer="Памуккале — это водоемы-террасы, образовавшиеся из травертина — легкой известковой горной породы. А с турецкого их название переводится как «хлопковый замок».")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? XI",
#                              t_q="Так это же Малиновое озеро в Алтайском крае.",
#                              f_q1="Какое красивое Розовое озеро Хиллиер на острове Мидл в Австралии.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIP82Xg8E-VCT7PPddO-1zGOsd172qOAAJt2TEb148JSy03z4oL9-4wAQADAgADeAADNAQ",
#                              big_answer="Эта природная достопримечательность находиться в России. Малиновое озеро в Михайловском районе — одно из 94 алтайских соленых озер. Розовый оттенок воде придает бактерия Serratia salinaria. Наиболее яркий цвет бывает весной.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? XII",
#                              t_q="Похоже на Соборную мечеть в Санкт-Петербурге.",
#                              f_q1="Конечно, же это Ансамбль мавзолеев Шахи Зинда в Самарканде.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIQhmXg-oNh1uNJgKxFmEibUUDL30KeAAJ-2TEb148JS_acg-MobMjpAQADAgADeAADNAQ",
#                              big_answer="Это Соборная мечеть в Санкт-Петербурге. Ее открыли в 1913 году, а закрыли в 1940-м. В здании устроили склад. Только в 1956 году мечеть была возвращена верующим.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? XIII",
#                              t_q="На фото Замок Майендорф в подмосковном поселке Барвиха.",
#                              f_q1="Это Средневековый замок Юссе на реке Эндр.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIQiGXg-qzxRpimmDMMPlE4yzJOO0TOAAJ_2TEb148JS4dYkXVZzbnrAQADAgADeAADNAQ",
#                              big_answer="Замок Майендорф, возведенный к 1885 году, находится в подмосковном поселке Барвиха. После революции здесь был организован интернат для сирот, затем санаторий Совнаркома «Барвиха». В настоящее время замок принадлежит Управлению делами Президента РФ.")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? XIV",
#                              t_q="Кажется, это гейзеры в Йеллоустонском национальном парке.",
#                              f_q1="Однозначно это вулканы Камчатки.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIQimXg-tK7e4nM6oBy8xWzrXRlgaIHAAKA2TEb148JS6ZWJMLOVgs7AQADAgADeAADNAQ",
#                              big_answer="Это Йеллоустонский национальный парк, который занимает площадь почти 9000 км² по меньшей мере 1283 гейзера (по исследованиям 2011 года).")
# data_client.set_new_quiz_ask(quiz_id=21,
#                              quiz_ask="Россия или нет? XV",
#                              t_q="Разумеется, это Ординская пещера в Пермском крае.",
#                              f_q1="Я думаю, что это пещера Сак-Актун («белая пещера») на полуострове Юкатан.",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="AgACAgIAAxkBAAIQjGXg-w59lZOUjY7j6rXnTPv2FrKtAAKC2TEb148JS2sX2KV8m5RmAQADAgADeAADNAQ",
#                              big_answer="Это ординская пещера в Пермском крае — самая большая гипсовая пещера в мире, заполненная водой. Длина ее подводной части — более 4 км.")
# data_client.set_new_quiz_ask(quiz_id=20,
#                              quiz_ask="Russia or No?",
#                              t_q="Lena",
#                              f_q1="Indigirka",
#                              f_q2="space",
#                              f_q3="space",
#                              image_id="",
#                              big_answer="")
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