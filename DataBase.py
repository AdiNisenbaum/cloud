import sqlite3


class DataBase:

    def __init__(self, db_name):
        """
        constructor
        :param db_name: the name of the data base
        """
        self.sqlite_file = db_name + '.db'
        self.connector = None  # pointer for data base
        self.cursor = None   # pointer for tables
        self._create_db()

    def _create_db(self):
        """
        create data base
        """
        self.connector = sqlite3.connect(self.sqlite_file)  # pointer for data base
        self.cursor = self.connector.cursor()   # pointer for tables
        self._create_table()

    def _create_table(self):
        """
        create a table for users
        """
        sql = f"CREATE TABLE IF NOT EXISTS users (user_name TEXT UNIQUE, password TEXT, mail TEXT)"
        self.cursor.execute(sql)

    def user_exists(self, user_name):
        """
        checks if user is already existing
        :param user_name: the user we want to check if exists
        :return: true if exist, false else
        """
        sql = f"SELECT(user_name) FROM users WHERE user_name = '{user_name}'"
        self.cursor.execute(sql)
        return len(self.cursor.fetchall()) != 0

    def mail_exists(self, mail):
        """
        checks if mail is already existing
        :param mail: the mail we want to check if already exists
        :return: true if exist, false else
        """
        sql = f"SELECT(mail) FROM users WHERE mail = '{mail}'"
        self.cursor.execute(sql)
        return len(self.cursor.fetchall()) != 0

    def insert_user(self, user_name, password, mail):
        # do I need to check if the email matches too?
        """
        inserts a user to the table if not exists
        :param user_name: the user name
        :param password: the password
        :param mail: the mail
        :return: true if inserts - user did not existed, false else
        """
        if not self.user_exists(user_name) and not self.mail_exists(mail):
            sql = f"INSERT INTO users (user_name, password, mail) VALUES ('{user_name}', '{password}', '{mail}')"
            self.cursor.execute(sql)
            self.connector.commit()
            return True
        else:
            return False

    def update_password(self, user_name, password):
        """
        Updating the users password
        :param user_name: the user name
        :param password: the user's password
        :return: True if updated password, false else
        """
        if self.user_exists(user_name):
            sql = f"UPDATE users SET password = '{password}' WHERE user_name = '{user_name}'"
            self.cursor.execute(sql)
            self.connector.commit()
            return True
        else:
            return False

    def update_mail(self, user_name, mail):
        """
        Updating the users password
        :param user_name: the user name
        :param mail: the user's mail
        :return: True if updated mail, false else
        """
        if self.user_exists(user_name):
            sql = f"UPDATE users SET mail = '{mail}' WHERE user_name = '{user_name}'"
            self.cursor.execute(sql)
            self.connector.commit()
            return True
        else:
            return False

    def remove_user(self, user):
        """
        removes user from table
        :param user: the user we wants to remove
        :return: True if deleted user, False else
        """
        if self.user_exists(user):
            sql = f"DELETE FROM users WHERE user_name = '{user}'"
            self.cursor.execute(sql)
            self.connector.commit()
            return True
        else:
            return False

    def get_password(self, user):
        """
        gets the user's password
        :param user: the user we wants to get the password of
        :return: the user's password if exists else None
        """
        if self.user_exists(user):
            sql = f"SELECT password FROM users WHERE user_name = '{user}'"
            self.cursor.execute(sql)
            password = self.cursor.fetchall()[0][0]
            return password
        else:
            return None

    def get_mail(self, user):
        """
        gets the user's mail
        :param user: the user we wants to get the mail of
        :return: the user's mail if exists else None
        """
        if self.user_exists(user):
            sql = f"SELECT mail FROM users WHERE user_name = '{user}'"
            self.cursor.execute(sql)
            mail = self.cursor.fetchall()[0][0]
            return mail
        else:
            return None
