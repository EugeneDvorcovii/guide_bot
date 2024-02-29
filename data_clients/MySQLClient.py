from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD
import pymysql
import time
import random
from config import host, user, password, db_version, BASE_IMAGE_ID
from languages.languages import languages


class DataClient:
    DATABASE_NAME = "guide_bot"

    table_title = ["town", "landmark", "fact", "user", "quiz_theme", "quiz", "quiz_ask"]
    drop_tables = ["quiz_ask", "quiz", "quiz_theme", "fact", "landmark", "town", "user"]

    def __init__(self) -> None:
        self.geolocator = Nominatim(user_agent="Bar Guide")
        self.con = pymysql.Connection(
            host=host,
            user=user,
            port=3306,
            password=password,
            use_unicode=True,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        self.create_db()
        print(self.create_all_tables())

    def create_db(self, db_title: str = DATABASE_NAME) -> bool:
        try:
            request = f"CREATE DATABASE IF NOT EXISTS {db_title};"
            with self.con.cursor() as cur:
                cur.execute(request)
                self.con.commit()
                return True
        except Exception:
            return False

    def create_table(self, request: str) -> bool:
        try:
            with self.con.cursor() as cur:
                cur.execute(request)
                self.con.commit()
                return True
        except Exception as ex:
            print(ex)
            return False

    def create_town_table(self) -> bool:
        table = "town"
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.{table} (id int AUTO_INCREMENT,
                      title VARCHAR(50),
                      version VARCHAR(20),

                      PRIMARY KEY(id),
                      UNIQUE(title))"""
        return self.create_table(request=request)

    def create_landmark_table(self) -> bool:
        table = "landmark"
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.{table} (id int AUTO_INCREMENT,
                      town_id int,
                      title VARCHAR(50),
                      image_id VARCHAR(100),
                      version VARCHAR(20),

                      PRIMARY KEY(id),
                      UNIQUE(title),
                      FOREIGN KEY(town_id) REFERENCES town(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_fact_table(self) -> bool:
        table = "fact"
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.{table} (id int AUTO_INCREMENT,
                      landmark_id int,
                      title VARCHAR(50),
                      text TEXT,
                      audio_id VARCHAR(100),
                      image_id VARCHAR(100),
                      version VARCHAR(20),

                      PRIMARY KEY(id),
                      UNIQUE(title),
                      FOREIGN KEY(landmark_id) REFERENCES landmark(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_user_table(self) -> bool:
        table = "user"
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.{table} (id int AUTO_INCREMENT,
                      name VARCHAR(50),
                      user_id VARCHAR(50),
                      status VARCHAR(20),
                      quiz_score int, 
                      version VARCHAR(20),

                      PRIMARY KEY(id),
                      UNIQUE(user_id))"""
        return self.create_table(request=request)

    def create_quiz_theme_table(self) -> bool:
        table = "quiz_theme"
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.{table} (id int AUTO_INCREMENT,
                      title VARCHAR(50),
                      description TEXT,
                      version VARCHAR(20),

                      PRIMARY KEY(id),
                      UNIQUE(title))"""
        return self.create_table(request=request)

    def create_quiz_table(self) -> bool:
        table = "quiz"
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.{table} (id int AUTO_INCREMENT,
                      theme_id int,
                      title VARCHAR(50),
                      description TEXT,
                      version VARCHAR(20),

                      PRIMARY KEY(id),
                      UNIQUE(title),
                      FOREIGN KEY(theme_id) REFERENCES quiz_theme(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_quiz_ask_table(self) -> bool:
        table = "quiz_ask"
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.{table} (id int AUTO_INCREMENT,
                      quiz_id int,
                      ask VARCHAR(500),
                      t_q VARCHAR(100),
                      f_q1 VARCHAR(100),
                      f_q2 VARCHAR(100),
                      f_q3 VARCHAR(100),
                      image_id VARCHAR(100),
                      version VARCHAR(20),

                      PRIMARY KEY(id),
                      UNIQUE(quiz_id, ask),
                      FOREIGN KEY(quiz_id) REFERENCES quiz(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_user_quiz_table(self) -> bool:
        table = "user_quiz"
        request = f"""CREATE TABLE IF NOT EXISTS {self.DATABASE_NAME}.{table} (id int AUTO_INCREMENT,
                      user_id int,
                      quiz_id int,
                      score int,
                      version VARCHAR(20),

                      PRIMARY KEY(id),
                      UNIQUE(user_id, quiz_id),
                      FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
                      FOREIGN KEY(quiz_id) REFERENCES quiz(id) ON DELETE CASCADE ON UPDATE CASCADE)"""
        return self.create_table(request=request)

    def create_all_tables(self) -> bool:
        result = (self.create_town_table()
                  & self.create_landmark_table()
                  & self.create_fact_table()
                  & self.create_user_table()
                  & self.create_quiz_theme_table()
                  & self.create_quiz_table()
                  & self.create_quiz_ask_table()
                  & self.create_user_quiz_table())
        return result

    def drop_table(self, table_title: str):
        request = f"DROP TABLE {self.DATABASE_NAME}.{table_title}"
        with self.con.cursor() as cur:
            cur.execute(request)
            self.con.commit()
        print("ok")

    def drop_all_tables(self) -> bool:
        try:
            for elem in self.drop_tables:
                self.drop_table(elem)
            return True
        except Exception as ex:
            print(ex)
            return False

    def set_new_data(self,
                     request: str,
                     record: list) -> bool:
        try:

            with self.con.cursor() as cur:
                cur.executemany(request, record)
                self.con.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def set_new_town(self,
                     title: str) -> bool:
        table = "town"
        request = f"INSERT INTO {self.DATABASE_NAME}.{table} (title, version) " \
                  "VALUES (%s, %s);"
        record = [(title, db_version)]
        return self.set_new_data(request=request, record=record)

    def set_new_landmark(self,
                         town_id: int,
                         title: str,
                         image_id: str) -> bool:
        table = "landmark"
        request = f"INSERT INTO {self.DATABASE_NAME}.{table} (town_id, title, image_id, version) " \
                  "VALUES (%s, %s, %s, %s);"
        record = [(town_id, title, image_id, db_version)]
        return self.set_new_data(request=request, record=record)

    def set_new_fact(self,
                     landmark_id: int,
                     title: str,
                     text: str,
                     audio_id: str,
                     image_id: str) -> bool:
        table = "fact"
        request = f"INSERT INTO {self.DATABASE_NAME}.{table} (landmark_id, title, text, audio_id, image_id, version) " \
                  "VALUES (%s, %s, %s, %s, %s, %s);"
        record = [(landmark_id, title, text, audio_id, image_id, db_version)]
        return self.set_new_data(request=request, record=record)

    def set_new_user(self,
                     name: str,
                     user_id: str,
                     ) -> bool:
        table = "user"
        request = f"INSERT INTO {self.DATABASE_NAME}.{table} (name, user_id, status, quiz_score, version) " \
                  "VALUES (%s, %s, %s, %s, %s);"
        record = [(name, user_id, "base", 0, db_version)]
        return self.set_new_data(request=request, record=record)

    def set_new_quiz_theme(self,
                           title: str,
                           description: str,
                           language: str) -> bool:
        table = "quiz_theme"
        request = f"INSERT INTO {self.DATABASE_NAME}.{table} (title, description, version, language) " \
                  "VALUES (%s, %s, %s, %s);"
        record = [(title, description, db_version, language)]
        return self.set_new_data(request=request, record=record)

    def set_new_quiz(self,
                     theme_id: int,
                     title: str,
                     description: str) -> bool:
        table = "quiz"
        request = f"INSERT INTO {self.DATABASE_NAME}.{table} (theme_id, title, description, version) " \
                  "VALUES (%s, %s, %s, %s);"
        record = [(theme_id, title, description, db_version)]
        return self.set_new_data(request=request, record=record)

    def set_new_quiz_ask(self,
                         quiz_id: int,
                         quiz_ask: str,
                         t_q: str,
                         f_q1: str,
                         f_q2: str,
                         f_q3: str,
                         image_id: str = None) -> bool:
        table = "quiz_ask"
        image_id = image_id if image_id else BASE_IMAGE_ID
        request = f"INSERT INTO {self.DATABASE_NAME}.{table} (quiz_id, ask, t_q, f_q1, f_q2, f_q3, image_id, version) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        record = [(quiz_id, quiz_ask, t_q, f_q1, f_q2, f_q3, image_id, db_version)]
        return self.set_new_data(request=request, record=record)

    def set_new_user_quiz(self,
                          user_id: int,
                          quiz_id: int) -> bool:
        table = "user_quiz"
        request = f"INSERT INTO {self.DATABASE_NAME}.{table} (user_id, quiz_id, score, version) " \
                  "VALUES (%s, %s, %s, %s);"
        record = [(user_id, quiz_id, 0, db_version)]
        return self.set_new_data(request=request, record=record)

    def get_info(self, request: str) -> list:
        with self.con.cursor() as cur:
            cur.execute(request)
            return cur.fetchall()

    def execute_request(self, request: str) -> bool:
        try:
            with self.con.cursor() as cur:
                cur.execute(request)
                self.con.commit()
            return True
        except Exception:
            return False

    def exist_elem(self, request: str) -> bool:
        with self.con.cursor() as cur:
            cur.execute(request)
            return len(cur.fetchall()) > 0

    def exist_user_quiz(self, user_id: int, quiz_id: int) -> [bool, int, int]:
        table = "user_quiz"
        request = f"SELECT * FROM {self.DATABASE_NAME}.{table} WHERE user_id = '{user_id}' AND quiz_id = '{quiz_id}';"
        with self.con.cursor() as cur:
            cur.execute(request)
            response = cur.fetchall()
            if len(response) > 0:
                return [True, response[0]["id"], response[0]["score"]]
            else:
                return [False, -1]

    def set_score_user_quiz(self, user_id: int, quiz_id: int, score: int):
        table = "user_quiz"
        result = self.exist_user_quiz(user_id=user_id, quiz_id=quiz_id)
        if result[0]:
            user_score = result[2] + score
            request = f"UPDATE {self.DATABASE_NAME}.{table} SET score='{user_score}' WHERE id = '{result[1]}';"
            result_2 = self.execute_request(request)
        else:
            self.set_new_user_quiz(user_id=user_id, quiz_id=quiz_id)

    ## Wrong function
    def get_data(self, table_title: str) -> str:
        request = f"SELECT * FROM {self.DATABASE_NAME}.{table_title};"
        return str(self.get_info(request))

    def get_all_data(self) -> str:
        text = ""
        for title in self.table_title:
            text += self.get_data(title) + "\n\n"
        return text

    def get_user_data(self):
        table = "user"
        request = f"SELECT * FROM {self.DATABASE_NAME}.{table};"
        return str(self.get_info(request))

    def get_user_quiz_data(self):
        table = "user_quiz"
        request = f"SELECT * FROM {self.DATABASE_NAME}.{table};"
        return str(self.get_info(request))

    #################
    # Program for program work
    #################

    def user_exist(self, user_id: str) -> bool:
        table = "user"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} where user_id = '{user_id}';"
        return self.exist_elem(request=request)

    def set_new_admin(self, user_id: str) -> bool:
        table = "user"
        request = f"UPDATE {self.DATABASE_NAME}.{table} SET status = 'admin' WHERE user_id = '{user_id}';"
        return self.execute_request(request=request)

    def town_exist(self, town_title: str) -> bool:
        table = "town"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} WHERE title = '{town_title}';"
        return self.exist_elem(request=request)

    def landmark_exist(self, landmark_title: str, town_id: int) -> bool:
        table = "landmark"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} WHERE title = '{landmark_title}' AND town_id = '{town_id}';"
        return self.exist_elem(request=request)

    def fact_exist(self, fact_title: str, landmark_id: int) -> bool:
        table = "fact"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} " \
                  f"WHERE title = '{fact_title}' AND landmark_id = '{landmark_id}';"
        return self.exist_elem(request=request)

    def user_quiz_exist(self, user_id: str, quiz_id: int) -> bool:
        user_id = self.get_user_id(user_id=user_id)
        table = "user_quiz"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} " \
                  f"WHERE user_id = '{user_id}' AND quiz_id = '{quiz_id}';"
        return self.exist_elem(request=request)

    def get_all_town_title(self) -> list:
        table = "town"
        request = f"SELECT title FROM {self.DATABASE_NAME}.{table};"
        data = [elem["title"] for elem in self.get_info(request)]
        return [len(data) > 0, data]

    def get_all_landmark_by_town_id(self, town_id: int) -> list:
        table = "landmark"
        request = f"SELECT title FROM {self.DATABASE_NAME}.{table} WHERE town_id = '{town_id}';"
        data = [elem["title"] for elem in self.get_info(request)]
        return [len(data) > 0, data]

    def get_town_id(self, town_title: str) -> int:
        table = "town"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} WHERE title = '{town_title}';"
        return self.get_info(request)[0]["id"]

    def get_landmark_id(self, town_id: int, landmark_title: str) -> int:
        table = "landmark"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} " \
                  f"WHERE title = '{landmark_title}' AND town_id = '{town_id}';"
        return self.get_info(request)[0]["id"]

    def get_quiz_theme_list(self, user_lang: str) -> [bool, list]:
        table = "quiz_theme"
        request = f"SELECT title FROM {self.DATABASE_NAME}.{table} WHERE language = '{user_lang}';"
        data = [elem["title"] for elem in self.get_info(request)]
        return [len(data) > 0, data]

    def get_quiz_list(self, theme_id: int) -> list:
        table = "quiz"
        request = f"SELECT title FROM {self.DATABASE_NAME}.{table} WHERE theme_id = '{theme_id}';"
        data = [elem["title"] for elem in self.get_info(request)]
        return [len(data) > 0, data]

    def get_quiz_theme_id(self, theme_title: str) -> int:
        table = "quiz_theme"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} WHERE title = '{theme_title}';"
        return self.get_info(request)[0]["id"]

    def get_quiz_id(self, theme_title: str) -> int:
        table = "quiz"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} WHERE title = '{theme_title}';"
        return self.get_info(request)[0]["id"]

    def get_quiz_title(self, quiz_id: int) -> str:
        table = "quiz"
        request = f"SELECT title FROM {self.DATABASE_NAME}.{table} WHERE id = '{quiz_id}';"
        return self.get_info(request)[0]["title"]

    def get_user_id(self, user_id: str) -> int:
        table = "user"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} WHERE user_id = '{user_id}';"
        return self.get_info(request)[0]["id"]

    def get_quiz_ask(self, quiz_id: int, ask_id: list) -> [bool, dict]:
        table = "quiz_ask"
        request = f"SELECT * FROM {self.DATABASE_NAME}.{table} WHERE quiz_id = '{quiz_id}';"
        data = self.get_info(request)
        index_ask = len(ask_id)
        # print(f"len asks: {index_ask}")
        return [True, data[index_ask]] if index_ask != len(data) else [False, dict()]

    def get_statistics(self, user_id: int, user_lang: str) -> str:
        table = "user_quiz"
        total_score = 0
        msg_back = f"{languages[user_lang]['stat_start']}\n"
        request = f"SELECT * FROM {self.DATABASE_NAME}.{table} WHERE user_id = '{user_id}';"
        for elem in self.get_info(request):
            quiz_title = self.get_quiz_title(elem["quiz_id"])
            msg_back += f"{languages[user_lang]['stat_1_step']}'{quiz_title}'" \
                        f"{languages[user_lang]['stat_2_step']}{elem['score']}{languages[user_lang]['stat_3_step']}\n"
            total_score += elem['score']
        msg_back += f"{languages[user_lang]['stat_total']}{total_score}."
        return msg_back

    def get_ask_id_list(self, quiz_id: int) -> list:
        table = "quiz_ask"
        request = f"SELECT id FROM {self.DATABASE_NAME}.{table} WHERE quiz_id = '{quiz_id}';"
        data = self.get_info(request)
        ask_id_list = list()
        for elem in data:
            ask_id_list.append(elem["id"])
        return ask_id_list

    def get_random_ask(self, quiz_id: int, ask_id_ready: list) -> dict:
        table = "quiz_ask"
        ask_id_list = self.get_ask_id_list(quiz_id=quiz_id)
        random_ask_id = random.choice(ask_id_list)
        while random_ask_id in ask_id_ready:
            random_ask_id = random.choice(ask_id_list)
        request = f"SELECT * FROM {self.DATABASE_NAME}.{table} WHERE id = '{random_ask_id}';"
        data = self.get_info(request)[0]
        return data

    def get_user_lang(self, user_id: str) -> str:
        table = "user"
        request = f"SELECT language FROM {self.DATABASE_NAME}.{table} WHERE user_id = '{user_id}';"
        data = self.get_info(request=request)[0]["language"]
        return data

    def change_user_lang(self, user_id: str, new_lang: str) -> bool:
        table = "user"
        request = f"UPDATE {self.DATABASE_NAME}.{table} SET language='{new_lang}' WHERE user_id = '{user_id}';"
        return self.execute_request(request=request)


    """
    Needed functions:
    set_new_user
    set_new_town
    set_new_landmark
    set_new_fact
    """








