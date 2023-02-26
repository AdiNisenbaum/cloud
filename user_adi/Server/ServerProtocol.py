

def unpack(data):
    """
    unpack the data and puts the opcode and is success msg in a tuple
    :param data: a string made out command and if it was a success
    :return: a tuple(opcode, list of data)
    """
    opcode = data[0:2]
    params = data[2:].split(",")
    return opcode, params


def pack_registration_msg(data):
    """
    pack a registration msg
    :param data: opcode and is a success
    :return: msg "001" or "000"
    """
    data = "00" + data
    return data


def pack_login_msg(data):
    """
    pack a login msg
    :param data: opcode and is a success
    :return: msg "011" or "010"
    """
    data = "01" + data
    return data


def pack_disconnect_msg(data):
    """
    pack a disconnect msg
    :param data: opcode and is a success
    :return: msg "021" or "020"
    """
    data = "02" + data
    return data


def pack_update_password_msg(data):
    """
    pack a update password msg
    :param data: opcode and is a success
    :return: msg "031" or "030"
    """
    data = "03" + data
    return data


def pack_upload_file_msg(data):
    """
    pack a update upload file msg
    :param data: opcode and is a success
    :return: msg "041" or "040"
    """
    data = "04" + data
    return data


def pack_delete_file_msg(data):
    """
    pack a delete file msg
    :param data: opcode and is a success
    :return: msg "061" or "060"
    """
    data = "06" + data
    return data


def pack_share_file_msg(data):
    """
    pack a share file msg
    :param data: opcode and is a success
    :return: msg "071" or "070"
    """
    data = "07" + data
    return data


def pack_change_name_msg(data):
    """
    pack a change name msg
    :param data: opcode and is a success
    :return: msg "081" or "080"
    """
    data = "08" + data
    return data


def pack_copy_file_msg(data):
    """
    pack a copy file msg
    :param data: opcode and is a success
    :return: msg "091" or "090"
    """
    data = "09" + data
    return data


def pack_open_file_msg(data):
    """
    pack a open file msg
    :param data: opcode and is a success
    :return: msg "101" or "100"
    """
    data = "10" + data
    return data


def pack_create_folder_msg(data):
    """
    pack a create folder msg
    :param data: opcode and is a success
    :return: msg "111" or "110"
    """
    data = "11" + data
    return data


def pack_transfer_folder_msg(data):
    """
    pack a transfer folder msg
    :param data: opcode and is a success
    :return: msg "121" or "120"
    """
    data = "12" + data
    return data


def pack_delete_folder_msg(data):
    """
    pack a delete folder msg
    :param data: opcode and is a success
    :return: msg "131" or "130"
    """
    data = "13" + data
    return data


def pack_download_folder_msg(data):
    """
    pack a download folder msg
    :param data: opcode and is a success
    :return: msg "141" or "140"
    """
    data = "14" + data
    return data


def pack_update_mail_msg(data):
    """
    pack a update mail msg
    :param data: opcode and is a success
    :return: msg "151" or "150"
    """
    data = "15" + data
    return data


def pack_download_file_msg(file_length, file_name):
    """
    :param file_length:
    :param file_name:
    :return:
    """
    opcode = "05"
    data = opcode + file_length + "," + file_name
    return data
