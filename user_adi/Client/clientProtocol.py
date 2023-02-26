
def unpack(data):
    """
    unpack the data and puts the opcode and is success msg in a tuple
    :param data: a string made out command and if it was a success
    :return: a tuple(opcode, list of data)
    """
    opcode = data[:2]
    is_ok = data[2:]
    command = [opcode, is_ok]
    return command


def pack_registration_msg(username, password, mail):
    """

    :param username:
    :param password:
    :param mail:
    :return:
    """
    opcode = "00"
    data = opcode + username + "," + password + "," + mail
    return data


def pack_login_msg(username, password):
    """

    :param username:
    :param password:
    :return:
    """
    opcode = "01"
    data = opcode + "," + username + "," + password
    return data


def pack_disconnect_msg():
    """
    client disconnected
    :return: 02
    """
    return "02"


def pack_update_password_msg(username, new_password):
    """

    :param username:
    :param new_password:
    :return:
    """
    opcode = "03"
    data = opcode + username + "," + new_password
    return data


def pack_upload_file_msg(file_name, content_size):
    """

    :param file_name:
    :param content_size:
    :return:
    """
    opcode = "04"
    data = opcode + file_name + "," + content_size
    return data


def pack_download_file_msg(file_name):
    """

    :param file_name:
    :return:
    """
    opcode = "05"
    data = opcode + file_name
    return data


def pack_delete_file_msg(file_name):
    """

    :param file_name:
    :return:
    """
    opcode = "06"
    data = opcode + file_name
    return data


def pack_share_file_msg(username, friend, file_name):
    """

    :param username:
    :param friend:
    :param file_name:
    :return:
    """
    opcode = "07"
    data = opcode + username + "," + friend + "," + file_name
    return data


def pack_rename_msg(file_name, new_file_name):
    """

    :param file_name:
    :param new_file_name:
    :return:
    """
    opcode = "08"
    data = opcode + file_name + "," + new_file_name
    return data


def pack_copy_file_msg(file_name):
    """

    :param file_name:
    :return:
    """
    opcode = "09"
    data = opcode + "," + file_name
    return data


def pack_open_file_msg(file_name):
    """

    :param file_name:
    :return:
    """
    opcode = "10"
    data = opcode + file_name
    return data


def pack_create_folder_msg(folder_name):
    """

    :param folder_name:
    :return:
    """
    opcode = "11"
    data = opcode + folder_name
    return data


def pack_transfer_folder_msg(folder_name, folder_tranfer_name):
    """

    :param folder_name:
    :param folder_tranfer_name:
    :return: 
    """
    opcode = "12"
    data = opcode + folder_name + "," + folder_tranfer_name
    return data


def pack_delete_folder_msg(folder_name):
    """

    :param folder_name:
    :return:
    """
    opcode = "13"
    data = opcode + folder_name
    return data


def pack_download_folder_msg(folder_name):
    """

    :param folder_name:
    :return:
    """
    opcode = "14"
    data = opcode + folder_name
    return data


def pack_update_mail_msg(username, new_mail):
    """

    :param username:
    :param new_mail:
    :return:
    """
    opcode = "15"
    data = opcode + username + "," + new_mail
    return data
