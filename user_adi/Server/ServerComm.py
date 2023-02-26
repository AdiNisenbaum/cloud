import socket
import threading
import select
from user_adi.Server import ServerProtocol


class ServerComm:
    """
    class to represent client  (communication)
    """
    def __init__(self, server_port, recv_q):
        """
        init the object
        :param server_port: port of communication
        """
        self.server_port = server_port  # the server's port
        self.socket = None  # the server's socket
        self.open_clients = {}  # a dictionary of all connected clients (their sockets) [socket] : [ip, key]
        self.msg_queue = recv_q  # a queue of all the receiving msg
        threading.Thread(target=self._main_loop).start()

    def change_key(self, client, ip):
        key = None
        self.open_clients[client] = [ip, key]
        pass

    def _main_loop(self):
        """
        connect to server
        """
        self.socket = socket.socket()
        self.socket.bind(('0.0.0.0', self.server_port))
        self.socket.listen(3)

        while True:
            rlist, wlist, xlist = select.select([self.socket] + list(self.open_clients.keys()), list(self.open_clients.keys()), [], 0.03)
            for current_socket in rlist:
                if current_socket is self.socket:
                    client, addr = self.socket.accept()
                    print(f"{addr[0]} - connected")
                    #self.open_clients[client] = addr[0]
                    threading.Thread(target=self.change_key, args=(client, addr[0],)).start()
                else:
                    try:
                        msg_len = int(current_socket.recv(5).decode())
                        data = current_socket.recv(msg_len).decode()
                    except Exception as e:
                        self._disconnect_client(current_socket)
                        print("ServerComm - _main_loop 1", str(e))
                    else:
                        if data == "":
                            self._disconnect_client((current_socket))
                        else:
                            # encrypt the msg
                            self.msg_queue.put((data, self.open_clients[current_socket][0]))

    def _disconnect_client(self, socket):
        """
        disconnect client
        :param socket: the client socket we want to disconnect
        """
        if socket in self.open_clients.keys():
            print(f"{self.open_clients[socket][0]} - disconnected")
            del self.open_clients[socket]
            socket.close()


    def _find_socket_by_ip(self, askip):
        soc = None
        for socket, (ip, key) in self.open_clients.items():
            if askip == ip:
                soc = socket
                break
        return soc

    def send_msg(self, msg, ip):
        """
        sends the msg to the client
        :param msg: the message to send
        :param socket: the socket to send the message to
        """

        client = self._find_socket_by_ip(ip)
        if client:
            #dec msg
            len_msg = len(msg)

            try:
                client.send(str(int(msg)).zfill(5).encode())
                client.send(msg.encode())
            except Exception as e:
                print("ServerComm - send_msg", str(e))
                self._disconnect_client(socket)

    def rcv_file(self, ip, file_name, file_size):
        """
        receiving the pic to the server
        :param ip:
        :param file_name:
        :param file_size:
        """

        client = self._find_socket_by_ip(ip)
        if client:
            # convert to integer
            file_size = int(file_size)
            data = bytearray()
            while len(data) < file_size:
                slice = file_size - len(data)
                if slice > 1024:
                    data.extend(client.recv(1024))
                else:
                    data.endswith(client.recv(slice))
                    break

            with open(file_name, "wb") as f:
                # write to the file the bytes we just received
                f.write(data)

            self.msg_queue.put(("getFile", (file_name, ip)))

    def send_file(self, file_path, ip):

        client = self._find_socket_by_ip(ip)
        if client:

            with open(file_path, 'rb') as client_file:
                file_content = client_file.read()

            packed = ServerProtocol.pack_download_file_msg(file_path, len(file_content))
            self.send_msg(packed, ip)

            # encrypt the file

            try:
                client.send(file_content)
            except Exception as e:
                print("ClientComm - send_msg", str(e))
                self._disconnect_client(client)


