import os
import shutil


def file_rename(username, old_file_name, new_file_name):
    """
    rename the file in the username folder
    :param username: the user name
    :param old_file_name: file to rename
    :param new_file_name: new name to rename
    :return: True if renamed, False else
    """
    try:
        path = r"T:\public\Adi\פרוייקט 2022-23\cloud" + "\\" + username + "\\" + old_file_name
        if os.path.isfile(path):
            new_path = r"T:\public\Adi\פרוייקט 2022-23\cloud" + "\\" + username + "\\" + new_file_name
            os.rename(path, new_path)
            return True
    except Exception as error:
        print("fileServer - file_rename - " + str(error))
        return False


def copy_file(username, file_name):
    """
    creates a copy from the file in the username folder
    :param username: the user name
    :param file_name: file to copy
    :return: True if copied, False else
    """
    counter = 1
    try:
        path = r"T:\public\Adi\פרוייקט 2022-23\cloud" + "\\" + username + "\\" + file_name
        file_name, file_extension = file_name.split(".")
        path_copy = r"T:\public\Adi\פרוייקט 2022-23\cloud" + "\\" + \
            username + "\\" + file_name + " - copy" + file_extension
        if os.path.isfile(path):
            while os.path.isfile(path_copy):
                path_copy = r"T:\public\Adi\פרוייקט 2022-23\cloud" + "\\" + username + "\\" + file_name + \
                        " - copy" + str(counter) + "." + file_extension
                counter += 1
            shutil.copyfile(path, path_copy)
            return True
    except Exception as error:
        print("fileServer - copy_file - " + str(error))
        return False


def share_file(username, friend_name, file_name):
    """
    copy the file from username folder to friend's folder
    :param username: the user that sends
    :param friend_name: the user that gets the file
    :param file_name: the file's name
    :return: True if file shared, False else
    """
    try:
        path = r"T:\public\Adi\פרוייקט 2022-23\cloud" + "\\" + username + "\\" + file_name
        if os.path.isfile(path):
            path_copy = r"T:\public\Adi\פרוייקט 2022-23\cloud" + "\\" + friend_name + "\\" + file_name
            shutil.copyfile(path, path_copy)
            return True
    except Exception as error:
        print("fileServer - share_file - " + str(error))
        return False


def delete_file(username, file_name):
    """
    delete the file in the username's folder
    :param username: the user that wants to delete a file
    :param file_name: the file to delete
    :return: True if file deleted, False else
    """
    try:
        path = r"T:\public\Adi\פרוייקט 2022-23\cloud" + "\\" + username + "\\" + file_name
        if os.path.isfile(path):
            os.remove(path)
            return True
    except Exception as error:
        print("fileServer - delete_file - " + str(error))
        return False
