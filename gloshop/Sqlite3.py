import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_id(self, autonum):
        with self.connection:
            responce = \
                self.cursor.execute(f"SELECT `id` FROM `order` WHERE `autonum` = ?", (autonum,)).fetchall()[0][0]
            return responce

    def get_user(self, id, *args):
        for arg in args:
            if args != id:
                with self.connection:
                    responce = \
                        self.cursor.execute(f"SELECT {arg} FROM `main_info` WHERE `id` = ?", (id,)).fetchmany(20)[0][0]
                    if responce == None:
                        return 'Не указано'
                    else:
                        return responce

    def get_basket(self, id, *args):
        for arg in args:
            if args != id:
                if args[0] == 'paid':
                    with self.connection:
                        print(1)
                        return self.cursor.execute("SELECT * FROM `shopping_basket` WHERE `paid`=='1'").fetchall()
                else:
                    with self.connection:
                        responce = \
                            self.cursor.execute(
                                f"SELECT {arg} FROM `shopping_basket` WHERE `id` = ? and `is_istanse`=='1'",
                                (id,)).fetchall()
                        if responce == None:
                            return 'Не указано'
                        else:
                            return responce

    def get_admins(self):
        with self.connection:
            return self.cursor.execute("SELECT id FROM `main_info` WHERE `status`=='admin'").fetchall()

    def successful_pay(self, autonum):
        with self.connection:
            return self.cursor.execute("UPDATE `shopping_basket` SET paid=? WHERE autonum=? ", (True, autonum))

    def successful_send(self, autonum):
        with self.connection:
            return self.cursor.execute("UPDATE `order` SET send=? WHERE autonum=? ", (True, autonum))

    def set_admin(self, id):
        with self.connection:
            return self.cursor.execute("UPDATE `main_info` SET status=? WHERE id=? ", ('admin',id))

    def user_exists(self, id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `main_info` WHERE `id` = ?', (id,)).fetchall()
            return bool(len(result))

    def add_user(self, id, name, surname, when_reg):
        with self.connection:
            return self.cursor.execute("INSERT INTO `main_info` (`id`,`name`,`surname`,`when_reg`) VALUES(?,?,?,?)",
                                       (id, name, surname, when_reg,))

    def add_thing(self, id, product_id, date_paid, cost, paid=False, count=1):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `shopping_basket` (`id`,`product`,`paid`,`date_paid`,`count`,`cost`) VALUES(?,?,?,?,?,?)",
                (id, product_id, paid, date_paid, count, cost))

    def get_order(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `order` WHERE `send`=='0'").fetchmany(10)

    def add_order(self, id, name_telegram, total_amount, name, city, street_line, state, index):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `order` (`id`,`name_telegram`,`total_amount`,`name`,`city`,`street_line`,`state`,`index`) VALUES(?,?,?,?,?,?,?,?)",
                (id, name_telegram, total_amount, name, city, street_line, state, index))

    def delete_basket(self, id, autonum):
        with self.connection:
            return self.cursor.execute("DELETE FROM `shopping_basket` WHERE autonum=? and `id`=?",
                                       (autonum, id,)).fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
