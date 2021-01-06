import os
from werkzeug._compat import text_type
from werkzeug._compat import PY2
import re

_filename_ascii_strip_re = re.compile(r"[..]")

def secure_filename(filename):
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.
    On windows systems the function also makes sure that the file is not
    named after one of the special device files.
    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >>> secure_filename(u'i contain cool \xfcml\xe4uts.txt')
    'i_contain_cool_umlauts.txt'
    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you abort or
    generate a random filename if the function returned an empty one.
    .. versionadded:: 0.5
    :param filename: the filename to secure
    """
    if isinstance(filename, text_type):
        from unicodedata import normalize

        filename = normalize("NFKD", filename).encode("ascii", "ignore")
        if not PY2:
            filename = filename.decode("ascii")
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
            print("filename= " + filename)
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = "_" + filename

    return filename

filename = "/../../../level1/test ~test.file"

sName = secure_filename(filename)

filename2 = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )

filename2 = re.sub(r'([/])\1+', r'\1', filename2)

filename3 = re.sub(r'\.\.', '', filename)
filename3 = re.sub(r'(/)\1+', r'\1', filename3)

print(sName)
print(filename2)
print(filename3)
