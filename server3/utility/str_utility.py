import os
import re
import unicodedata
import string
import random
import base64
from Crypto import Random
from Crypto.Cipher import AES
from mongoengine import DoesNotExist
from werkzeug._compat import text_type
from werkzeug._compat import PY2
from pypinyin import pinyin, Style

uid_chars = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')

_ascii_strip_re = {
    'user': re.compile(r'[^A-Za-z0-9]'),
    'app': re.compile(r'[^A-Za-z0-9-]'),
    'module': re.compile(r'[^A-Za-z0-9]'),
    'dataset': re.compile(r'[^A-Za-z0-9-]'),
}

split_re = {
    'user': '[^A-Za-z0-9]',
    'app': '[^A-Za-z0-9-]',
    'module': '[^A-Za-z0-9]',
    'dataset': '[^A-Za-z0-9-]',
}
connector_re = {
    'user': '',
    'app': '-',
    'module': '',
    'dataset': '-',
}
AKEY = '27cfbc4d262403839797636105d0a476'  # AES key must be either 16, 24, or 32 bytes long

# iv = Random.new().read(AES.block_size)
iv = 'This is an IV456'


def encode(message):
    obj = AES.new(AKEY.encode("utf8"), AES.MODE_CFB, iv.encode("utf8"))
    message = bytes(message, encoding="utf8")
    return base64.urlsafe_b64encode(obj.encrypt(message)).decode("utf-8")


def decode(cipher):
    obj2 = AES.new(AKEY, AES.MODE_CFB, iv)
    if not isinstance(cipher, str):
        cipher = cipher.encode("uft-8")
    return obj2.decrypt(base64.urlsafe_b64decode(cipher))


def generate_args_str(args):
    array = ["%s=%s" % (k, (v if not isinstance(v, str) else "'%s'" % v))
             for k, v in args.items()]
    return ', '.join(array)


# def remove_dot(string):
#     string.replace('.', '')
#     return string


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    if value == '':
        value = 'field' + rand_str(3)

    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip()
    return re.sub(r'[-\s]+', '-', value)


def rand_str(length):
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=length))


def split_without_empty(string):
    return [x.strip() for x in string.split(',') if x]


# werkzeug.utils
def secure_name(filename, type='user'):
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.
    On windows systems the function also makes sure that the file is not
    named after one of the special device files.
    >> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >> secure_filename(u'i contain cool \xfcml\xe4uts.txt')
    'i_contain_cool_umlauts.txt'
    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you abort or
    generate a random filename if the function returned an empty one.
    .. versionadded:: 0.5
    :param filename: the filename to secure
    :param type: ['user', 'app', 'module', 'dataset']
    """
    if isinstance(filename, text_type):
        filename = ''.join([p[0] for p in pinyin(filename, style=Style.TONE2)])
        from unicodedata import normalize
        filename = normalize('NFKD', filename).encode('ascii', 'ignore')
        if not PY2:
            filename = filename.decode('ascii')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
    filename = str(
        re.compile(r'[^A-Za-z0-9-_]').sub('', connector_re[type].join(
            re.split('[\-_ ]+', filename)))).strip(
        connector_re[type]).lower()

    return filename


def short_uid(uid_length):
    count = len(uid_chars) - 1
    c = ''
    for i in range(0, uid_length):
        c += uid_chars[random.randint(0, count)]
    return c


def gen_rand_name(name, get_func, times=1, **kwargs):
    from server3.constants import RCUserDoesNotExists
    for i in range(times):
        try:
            get_func(name, **kwargs)
        except (DoesNotExist, RCUserDoesNotExists):
            break
        else:
            name += short_uid(2)
    return name


def gen_rand_str(N=8, low=False):
    if low:
        return ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=N))
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
