import random
import string
import os


def create_file(namef, path, size):
    if not size.isdigit():
        if size.endswith('KB'):
            s1 = size.split('KB')
            size1 = int(s1[0]) * 1024
            token = ''.join(random.choice(string.ascii_uppercase +
                                          string.ascii_lowercase +
                                          string.digits) for _ in range(size1))
        elif size.endswith('MB'):
            s1 = size.split('MB')
            size1 = int(s1[0])*1048567
            token = ''.join(random.choice(string.ascii_uppercase +
                                          string.ascii_lowercase +
                                          string.digits) for _ in range(size1))
        elif size.endswith('GB'):
            s1 = size.split('GB')
            size1 = int(s1[0]) * 1073741824
            token = ''.join(random.choice(string.ascii_uppercase +
                                          string.ascii_lowercase +
                                          string.digits) for _ in range(size1))
        else:
            size1 = int(size[:-1])
            token = ''.join(random.choice(string.ascii_uppercase +
                                          string.ascii_lowercase +
                                          string.digits) for _ in range(size1))

    else:
        token = ''.join(random.choice(string.ascii_uppercase +
                                      string.ascii_lowercase +
                                      string.digits) for _ in range(int(size)))

    file_path = os.path.join(namef, path)
    file = open(file_path, "w")
    file.write(token)
    file.close()


create_file("test1.txt", "F:\\torrent", '10KB')
create_file("test2.txt", "F:\\torrent", '1024')
create_file("test11.txt", "F:\\torrent", '2MB')
create_file("test21.txt", "F:\\torrent", '1B')
