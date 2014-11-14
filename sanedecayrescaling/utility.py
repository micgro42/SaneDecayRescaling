import os
def open_file_safely(path_to_file, modus):
    """tries top open the file and exit on fail"""

    try:
        open_file = open(path_to_file, modus)
    except IOError:
        print 'cannot open', path_to_file
        raise SystemExit(os.EX_IOERR)
    return open_file

def create_dirs(number_of_dir, path_to_base_dir):
    """creates directories"""

    if not os.path.isdir(path_to_base_dir):
        os.mkdir(path_to_base_dir)

    if (number_of_dir > 99):
        for i in range(100,number_of_dir):
            os.mkdir(path_to_base_dir + '/' + str(i))

    if (number_of_dir > 99):
        for i in range(10,99):
            os.mkdir(path_to_base_dir + '/0' + str(i))
    elif (9 < number_of_dir and number_of_dir < 99):
        for i in range(10,number_of_dir):
            os.mkdir(path_to_base_dir + '/0' + str(i))

    if (number_of_dir > 9):
        for i in range(0,9):
            os.mkdir(path_to_base_dir + '/00' + str(i))
    else:
        for i in range(0,number_of_dir):
            os.mkdir(path_to_base_dir + '/00' + str(i))


class ParseError(Exception):
    def __init__(self, line , msg = 'some parsing went wrong'):
        self.line = line
        self.msg = msg

class BadData(Exception):
    def __init__(self, line, daughters, msg = 'The decay is not usefully listed.'):
        self.line = line
        self.msg = msg
        self.daughters = daughters
