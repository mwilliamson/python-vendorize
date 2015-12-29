import os

                    
def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)


def ensure_file_exists(path):
    if not os.path.exists(path):
        mkdir_p(os.path.dirname(path))
        open(path, "w").close()
