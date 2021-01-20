# build_dir.py
import os


def build_dir(curPath):
    directoryDict = {}
    with os.scandir(curPath) as directory:
        for entry in directory:
            #dont include shortcuts and hidden files
            if not entry.name.startswith('.'):
                #stat dict reference:
                #https://docs.python.org/2/library/stat.html
                fileStats = entry.stat()
                directoryDict[entry.name] = {"is_dir" : entry.is_dir(),
                                            "size" : fileStats.st_size}
    return directoryDict