import os
def open_file_safely(path_to_file, modus):
    """tries top open the file and exit on fail"""

    try:
        open_file = open(path_to_file, modus)
    except IOError:
        print 'cannot open', path_to_file
        raise SystemExit(os.EX_IOERR)
    return open_file