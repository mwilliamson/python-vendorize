import os
import shutil
import io
import tarfile
import urllib2

                    
def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)


def ensure_file_exists(path):
    if not os.path.exists(path):
        mkdir_p(os.path.dirname(path))
        open(path, "w").close()


def copy(source, destination):
    shutil.copy2(source, destination)


def copy_recursive(source, destination):
    for (dirpath, dirnames, filenames) in os.walk(source):
        relative_dirpath = os.path.relpath(dirpath, source)
        target_dirpath = os.path.join(destination, relative_dirpath)
        mkdir_p(target_dirpath)
        for filename in filenames:
            copy(os.path.join(dirpath, filename), target_dirpath)


def download_tarball(url, target_directory):
    tarball_fileobj = io.BytesIO(urllib2.urlopen(url).read())
    tarball = tarfile.open(fileobj=tarball_fileobj)
    tarball.extractall(target_directory)
