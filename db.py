import  pymysql
from config import host , user , password , db_name

try:
        connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor)
        try:
                with connection.cursor() as cursor:
                        query = f"SHOW TABLES"
                        cursor.execute(query)
                        connection.commit()
        finally:
                connection.close()
except Exception as ex:
        print(f"Ошибка {ex}")
def NewUser(name):
        try:
                connection = pymysql.connect(
                        host=host,
                        port=3306,
                        user=user,
                        password=password,
                        database=db_name,
                        cursorclass=pymysql.cursors.DictCursor)
                try :
                        with connection.cursor() as cursor:
                                query = f"INSERT INTO `user` ( `name` ) VALUES ('{name}')"
                                cursor.execute(query)
                                connection.commit()
                finally:
                        connection.close()
        except Exception as ex:
                print (f"Ошибка {ex}")

def add_product(name, category,cost):
        try:
                connection = pymysql.connect(
                        host=host,
                        port=3306,
                        user=user,
                        password=password,
                        database=db_name,
                        cursorclass=pymysql.cursors.DictCursor)
                try :
                        with connection.cursor() as cursor:
                                query = f"INSERT INTO `products` (`name`,`category`,`cost` ) VALUES ('{name}', '{category}','{cost}' )"
                                cursor.execute(query)
                                connection.commit()
                finally:
                        connection.close()
        except Exception as ex:
                print (f"Ошибка {ex}")

def user_category():
        try:
                connection = pymysql.connect(
                        host=host,
                        port=3306,
                        user=user,
                        password=password,
                        database=db_name,
                        cursorclass=pymysql.cursors.DictCursor)
                try:
                        with connection.cursor() as cursor:
                                query = f"SELECT `name` FROM `user`"
                                cursor.execute(query)
                                connection.commit()
                                rows = cursor.fetchall()
                                all_user = []
                                for i in rows:
                                        all_user.append(i['name'])
                                        query = f"SELECT `drink`, `milky`,`alcohol`, `baby_food` FROM `user` WHERE `name` = '{i['name']}'"
                                        cursor.execute(query)
                                        connection.commit()
                                        rows = cursor.fetchall()
                                        for i1 in rows[0]:
                                              rows[0]
                                print(all_user)
                finally:
                        connection.close()
        except Exception as ex:
                print(f"Ошибка {ex}")

def discount(name):
        try:
                connection = pymysql.connect(
                        host=host,
                        port=3306,
                        user=user,
                        password=password,
                        database=db_name,
                        cursorclass=pymysql.cursors.DictCursor)
                try:
                        with connection.cursor() as cursor:
                                query = f"SELECT `discount` FROM `user` WHERE `name` = '{name}'"
                                cursor.execute(query)
                                rows = cursor.fetchall()
                                discount = rows[0]['discount']

                                query = f"SELECT `category` FROM `user` WHERE `name` = '{name}'"
                                cursor.execute(query)
                                rows = cursor.fetchall()
                                category = rows[0]['category']

                                if category == 'alcohol':
                                        category = 'Алкоголь'
                                if category == 'baby_food':
                                        category = 'Товары для детей'
                                if category == 'drink':
                                        category = 'Напитки'
                                if category == 'milky':
                                        category = 'Молочная продукция'


                                query = f"SELECT `name` , `cost` FROM `products` WHERE `category` = '{category}'"
                                cursor.execute(query)
                                rows = cursor.fetchall()
                                personal = {}
                                for i in range(4):
                                        name = rows[i]['name']
                                        discount1 = float(f"0.{discount}")
                                        cost = int(rows[i]['cost']) - (int(rows[i]['cost']) * discount1)
                                        personal[name] = {'Цена со скидкой': cost}
                                return personal
                                connection.commit()
                finally:
                        connection.close()
        except Exception as ex:
                print(f"Ошибка {ex}")
