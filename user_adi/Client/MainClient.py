from user_adi.Client.ClientComm import ClientComm
import queue
from . import clientProtocol


class MainClient:
    CLIENT_PORT = 2222
    comm = ClientComm(CLIENT_PORT, "0.0.0.0")
    recv_q = queue.Queue()

    def handle_registration_msg(self, username, password, mail):
        pass

    def handle_login_msg(self, username, password):
        pass

    def handle_disconnect_msg(self):
        pass

    def handle_update_password_msg(self, username, new_password):
        # TODO hash new password
        pass

    def handle_upload_file_msg(self, file_name, content_size):
        pass

    def handle_download_file_msg(self, file_name):
        pass

    def handle_delete_file_msg(self, file_name):
        pass

    def handle_share_file_msg(self, username, friend, file_name):
        pass

    def handle_rename_file_msg(self, username, file_name, new_file_name):
        pass

    def handle_copy_file_msg(self, username, file):
        pass

    def handle_open_file_msg(self, file):
        pass

    def handle_create_folder_msg(self, folder):
        pass

    def handle_transfer_folder_msg(self, folder):
        pass

    def handle_delete_folder_msg(self, folder):
        pass

    def handle_download_folder_msg(self, folder):
        pass

    def handle_update_mail_msg(self, username, new_mail):
        pass
    operations = {"00": handle_registration_msg, "01": handle_login_msg, "02": handle_disconnect_msg,
                  "03": handle_update_password_msg, "04": handle_upload_file_msg, "05": handle_download_file_msg,
                  "06": handle_delete_file_msg, "07": handle_share_file_msg, "08": handle_rename_file_msg,
                  "09": handle_copy_file_msg, "10": handle_open_file_msg, "11": handle_create_folder_msg,
                  "12": handle_transfer_folder_msg, "13": handle_delete_folder_msg, "14": handle_download_folder_msg,
                  "15": handle_update_mail_msg}
    
    def main(self):
        pass
    
    def main_recv(self):
        while self.recv_q.get():
            # TODO decrypt msg
            msg = self.recv_q.get()
            command = clientProtocol.unpack(msg)  # [opcode, is_ok]
            opcode = command[0]
            function = self.operations.get(opcode)
            function(command[1])
