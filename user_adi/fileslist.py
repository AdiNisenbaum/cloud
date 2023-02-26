import os


def get_user_files(username):
    '''

    :param username: name of the user folder
    :return: string with all of the contains separate by ,
    '''
    files = []
    for x,y,z in os.walk(f"T:\public\Adi\{username}"):
        files.append(x)
        for dir in y:
           files.append(dir)
        for file in z:
            files.append(file)

    return ','.join(x for x in files)


def build_files_dic(filestr):
    files = filestr.split(",")
    print(files)
    files_dic = {}
    key = None
    for file in files:
        if "\\" in file:
            if key:
                files_dic[key].append("back")
            files_dic[file]= []
            key = file
        else:
            files_dic[key].append(file)

    files_dic[key].append("back")
    files_dic[files[0]].remove("back")

    print(files_dic)

    #to find files in directory when user click on dir
    #current_dir
    # if dir is choose
    # current_dir = key+\\+choosen dir
    # if back is choose
    # current_dir = current_dir[:current_dir.rfind("\\")







if __name__ == '__main__':
    files = get_user_files("username1")
    print(files)
    build_files_dic(files)