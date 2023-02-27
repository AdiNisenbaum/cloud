from user_adi.Server.ServerComm import ServerComm
import queue
from user_adi.Server import ServerProtocol, FileServer
from DataBase import DataBase
import threading
import os
import shutil


class MainServer:

    def __init__(self):
        self.send_q = queue.Queue()
        self.recv_q = queue.Queue()
        self.comm = ServerComm(1000, self.recv_q)
        self.db = DataBase('cloud')
        self.users = {}

        threading.Thread(target=self._recv_loop).start()
        threading.Thread(target=self._send_loop).start()

    def handle_registration_msg(self, ip, data):
        """
        Add username to db (after hash the pass) and put ans in send_q
        :param ip:
        :param data: a list of [username, password, mail]
        """
        username, password, mail = data

        status = self.db.insert_user(username, password, mail)
        if status:
            ans = "0"
            self.users[ip] = username
        else:
            ans = "1"
        # TODO password = hashed password
        self.send_q.put((ip,ServerProtocol.pack_registration_msg(ans)))

    def handle_login_msg(self, ip, data):
        """
        checks if username exists in db and put ans in send_q
        :param ip:
        :param data:
        """
        username, password = data
        # TODO password = hashed password
        password_check = self.db.get_password(username)

        if password_check is None:
            ans = "1"
        elif password_check == password:
            ans = "0"
            self.users[ip] = username
            # TODO insert into self_q all files of user.
        else:
            ans = "1"
        self.send_q.put((ip, ServerProtocol.pack_login_msg(ans)))

    def handle_disconnect_msg(self):
        pass

    def handle_update_password_msg(self, data):
        username, new_password = data
        # TODO new_password = hashed new_password
        status = self.db.update_password(username, new_password)
        if status:
            ans = "0"
            # TODO insert into self_q all files of user.
        else:
            ans = "1"
        self.send_q.put(ServerProtocol.pack_update_password_msg(ans))

    def handle_upload_file_msg(self, ip, data):
        file_name, content_size = data
        try:
            user = self.users[ip]
            path = r"T:\public\Adi\פרוייקט 2022-23\cloud" + "\\" + user + "\\" + file_name
            self.comm.rcv_file(ip, path, content_size)
            ans = "0"
        except Exception as Error:
            ans = "1"
            print("Error in MainServer - handle_upload_file_msg" + str(Error))
        self.send_q.put((ip, ServerProtocol.pack_upload_file_msg(ans)))

    def handle_download_file_msg(self, data):
        file_name = data
        # call merry
        pass

    def handle_delete_file_msg(self, ip, data):
        username, file_name = data
        status = FileServer.delete_file(username, file_name)
        if status:
            ans = "0"
            self.users[ip] = username
        else:
            ans = "1"
        self.send_q.put((ip, ServerProtocol.pack_delete_file_msg(ans)))

    def handle_share_file_msg(self, ip, data):
        username, friend, file_name = data
        status = FileServer.share_file(username, friend, file_name)
        if status:
            ans = "0"
        else:
            ans = "1"
        self.send_q.put((ip, ServerProtocol.pack_share_file_msg(ans)))

    def handle_rename_file_msg(self, ip, data):
        username, file_name, new_file_name = data
        status = FileServer.file_rename(username, file_name, new_file_name)
        if status:
            ans = "0"
            self.users[ip] = username
        else:
            ans = "1"
        self.send_q.put((ip, ServerProtocol.pack_rename_msg(ans)))

    def handle_copy_file_msg(self, ip, data):
        username, file = data
        status = FileServer.copy_file(username, file)
        if status:
            ans = "0"
            self.users[ip] = username
        else:
            ans = "1"
        self.send_q.put((ip, ServerProtocol.pack_copy_file_msg(ans)))

    def handle_open_file_msg(self, data):
        file = data
        pass

    def handle_create_folder_msg(self, ip, data):
        folder = data
        # user = self.users[ip]
        try:
            os.mkdir(folder)    # puts default mode --> os.mkdir(path, mode)
            status = "0"
        except FileExistsError:
            print("Error in MainServer - handle_create_folder_msg - FileExistsError")
            status = "1"
        self.send_q.put(ip, ServerProtocol.pack_create_folder_msg(status))

    def handle_transfer_folder_msg(self, ip, data):
        folder, to_folder = data
        try:
            folder_name = folder.split("\\")[-1]
            folder.replace(folder_name, to_folder)
            status = "0"
        except Exception as Error:
            print("Error in MainServer - handle_transfer_folder_msg" + str(Error))
            status = "1"
        self.send_q.put(ip, ServerProtocol.pack_transfer_folder_msg(status))

    def handle_delete_folder_msg(self, ip, data):
        folder = data
        try:
            shutil.rmtree(folder)
            status = "0"
        except Exception as Error:
            print("Error in MainServer - handle_delete_folder_msg" + str(Error))
            status = "1"
        self.send_q.put(ip, ServerProtocol.pack_delete_folder_msg(status))

    def handle_download_folder_msg(self, folder):
        pass

    def handle_update_mail_msg(self, ip, data):
        username, new_mail = data

        status = self.db.update_mail(username, new_mail)
        if status:
            ans = "0"
            self.users[ip] = username
        else:
            ans = "1"
        self.send_q.put((ip, ServerProtocol.pack_update_mail_msg(ans)))

    def _recv_loop(self):
        # TODO add to variables encrypt_decrypt
        # TODO encrypt_decrypt attribute
        # TODO decrypt the msg

        operations = {"00": self.handle_registration_msg, "01": self.handle_login_msg, "02": self.handle_disconnect_msg,
                      "03": self.handle_update_password_msg,
                      "04": self.handle_upload_file_msg, "05": self.handle_download_file_msg,
                      "06": self.handle_delete_file_msg,
                      "07": self.handle_share_file_msg, "08": self.handle_rename_file_msg,
                      "09": self.handle_copy_file_msg,
                      "10": self.handle_open_file_msg, "11": self.handle_create_folder_msg,
                      "12": self.handle_transfer_folder_msg, "13": self.handle_delete_folder_msg,
                      "14": self.handle_download_folder_msg,
                      "15": self.handle_update_mail_msg}

        while True:
            data, ip = self.recv_q.get()

            if data == "getFile":
                file_name, userip = ip
                user = self.users[userip]
                # copy file_name to user dir
                self.handle_copy_file_msg(user, file_name)

            else:
                opcode, params = ServerProtocol.unpack(data)
                if opcode in operations.keys():
                    operations[opcode](ip, params)

    def _send_loop(self):
        """
        In a loop get message from send_q and:
        1.encrypt
        2. send by comm
        :return:
        """
        while True:
            ip, msg = self.send_q.get()
            self.comm.send_msg(msg, ip)


if __name__ == '__main__':
    MainServer()
