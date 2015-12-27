import os
import shutil

                    
def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)


def copy(source, destination):
    shutil.copy2(source, destination)


def copy_recursive(source, destination):
    for (dirpath, dirnames, filenames) in os.walk(source):
        relative_dirpath = os.path.relpath(dirpath, source)
        target_dirpath = os.path.join(destination, relative_dirpath)
        mkdir_p(target_dirpath)
        for filename in filenames:
            copy(os.path.join(dirpath, filename), target_dirpath)
