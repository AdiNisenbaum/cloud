import socket
import threading
import select
import queue
from user_adi.Client import clientProtocol


class ClientComm:
    """
    class for client attribute
    """
    def __init__(self, client_port, server_ip, recv_q):
        """
        init the object
        :param client_port: port of communication
        """
        self.client_port = client_port  # the server's port
        self.socket = socket.socket()  # the server's socket
        self.server_ip = server_ip
        self.msg_queue = recv_q  # a queue of all the receiving msg
        threading.Thread(target=self._main_loop).start()


    def _main_loop(self):
        """
        connect to server and put all incoming msg in msg_q
        """
        try:
            self.socket.connect((self.server_ip,self.client_port))
        except Exception as e:
            print(str(e))
            self._disconnect()

        # change_key

        while True:
            try:
                msg_len = int(self.socket.recv(5).decode())
                data = self.socket.recv(msg_len).decode()
            except Exception as e:
                print("ClientComm - _main_loop 1", str(e))
                self._disconnect()
            else:
                if data == "":
                    self._disconnect()
                else:
                    self.msg_queue.put(data)


    def send(self, msg):
        """
        send's a msg to server
        :param msg: a msg to send to the server
        """

        # enc_msg

        try:
            self.socket.send(str(len(msg)).zfill(5).encode())
            self.socket.send(msg.encode())
        except Exception as e:
            print("ClientComm - send_msg", str(e))
            self._disconnect()
        else:
            print(f"send to {self.socket} - {msg}")

    def _disconnect(self):
        print("server is down")
        self.socket.close()

    def send_file(self, file_path: str):
        file_name = file_path.split("\\")[-1]

        with open(file_path, 'rb') as client_file:
            file_content = client_file.read()

        packed = clientProtocol.pack_upload_file_msg(file_name, len(file_content))
        self.send(packed)

        # encrypt the file

        try:
            self.socket.send(file_content)
        except Exception as e:
            print("ClientComm - send_msg", str(e))
            self._disconnect()

    def rcv_file(self, file_name, file_size):
        """
        receiving the pic to the server
        :param client_socket:
        :param file_name:
        :param file_size:
        """

        # convert to integer
        file_size = int(file_size)
        data = bytearray()
        while len(data) < file_size:
            slice = file_size - len(data)
            if slice > 1024:
                data.extend(self.socket.recv(1024))
            else:
                data.endswith(self.socket.recv(slice))
                break

        with open(file_name, "wb") as f:
            # write to the file the bytes we just received
            f.write(data)

        self.msg_queue.put(("getFile", file_name))

