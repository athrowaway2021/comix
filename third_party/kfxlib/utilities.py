from __future__ import (unicode_literals, division, absolute_import, print_function)

import atexit
import base64
import collections
import functools
import gzip
import hashlib
import html
import io
import json
import locale
import logging
import posixpath
import os
import random
import re
import shutil
import string
import struct
import sys
import time
import urllib.parse
import uuid
import zipfile

from .message_logging import log

try:
    from calibre.constants import numeric_version as calibre_numeric_version
except ImportError:
    calibre_numeric_version = None


__license__ = "GPL v3"
__copyright__ = "2016-2023, John Howell <jhowell@acm.org>"


MAX_TEMPDIR_REMOVAL_TRIES = 60

PLATFORM_NAME = sys.platform.lower()
IS_MACOS = "darwin" in PLATFORM_NAME
IS_WINDOWS = "win32" in PLATFORM_NAME or "win64" in PLATFORM_NAME
IS_LINUX = not (IS_MACOS or IS_WINDOWS)
LOCALE_ENCODING = locale.getdefaultlocale()[1] or "utf8"
PATH_SEPARATOR = ";" if IS_WINDOWS else ":"
INTERNAL_FILE_SCHEME = "internal-file"


UUID_RE = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
UUID_MATCH_RE = r"^%s$" % UUID_RE

ZIP_SIGNATURE = b"\x50\x4B\x03\x04"

tempdir_ = None
atexit_set_ = False
ALPHA_NUMERIC = string.ascii_lowercase + string.digits


try:
    from calibre.ptempfile import PersistentTemporaryDirectory
    calibre_temp = True
except ImportError:
    import tempfile
    calibre_temp = False


def tempdir():
    global tempdir_
    global atexit_set_

    if tempdir_ is not None and not os.path.isdir(tempdir_):
        raise Exception("Temporary directory is missing: %s" % tempdir_)

    if tempdir_ is None:
        if calibre_temp:
            tempdir_ = PersistentTemporaryDirectory()
        else:
            tempdir_ = tempfile.mkdtemp()

            if not atexit_set_:
                atexit.register(temp_file_cleanup)
                atexit_set_ = True

    return tempdir_


def temp_file_cleanup():
    global tempdir_

    if tempdir_ is not None and not calibre_temp:
        tries = 0
        while (tempdir_ and tries < MAX_TEMPDIR_REMOVAL_TRIES):
            if tries > 0:
                time.sleep(1)

            try:
                shutil.rmtree(tempdir_)
                tempdir_ = None
            except Exception:
                tries += 1

        if tempdir_:
            log.error("Failed to remove temp directory: %s" % tempdir_)

            tempdir_ = None


def temp_filename(ext, data=None):
    if ext:
        ext = "." + ext

    unique = "".join(random.choice(ALPHA_NUMERIC) for _ in range(20))
    filename = os.path.join(tempdir(), unique + ext)

    if data is not None:
        file_write_binary(filename, data)

    return filename


def create_temp_dir():
    dirname = temp_filename("")
    os.mkdir(dirname)
    return dirname


def type_name(x):
    return type(x).__name__


def natural_sort_key(s):
    return "".join(["00000000"[len(c):] + c if c.isdigit() else c for c in re.split(r"([0-9]+)", s.lower())])


def list_keys(a_dict):
    return list_symbols(a_dict.keys())


def list_symbols(a_iter):
    return ", ".join(sorted(unicode_list(a_iter)))


def list_symbols_unsorted(a_iter):
    return ", ".join(unicode_list(a_iter))


def list_truncated(a_iter, max_allowed=10):
    return ", ".join(truncate_list(sorted(unicode_list(a_iter)), max_allowed))


def unicode_list(lst):
    return [str(s) for s in lst]


def truncate_list(lst, max_allowed=10):
    return lst if len(lst) <= max_allowed else lst[:max_allowed] + ["... (%d total)" % len(lst)]


def remove_duplicates(lst):
    return list(collections.OrderedDict.fromkeys(lst))


def bytes_to_separated_hex(data, sep=" "):
    return sep.join("%02x" % b for b in data)


def quote_name(s):
    return "\"%s\"" % s if ("," in s or " " in s) else s


def check_empty(a_dict, dict_name):
    if len(a_dict) > 0:
        try:
            extra_data = repr(a_dict)
        except Exception:
            extra_data = None

        if (extra_data is None) or (len(extra_data) > 1024):
            extra_data = "%s (keys only)" % list_keys(a_dict)

        log.error("%s has extra data: %s" % (str(dict_name), extra_data))
        a_dict.clear()


def json_serialize(data, sort_keys=False, indent=4, separators=(",", ": ")):
    return json.dumps(data, indent=indent, separators=separators, sort_keys=sort_keys, default=lambda o: o.__dict__)


def json_serialize_compact(data, sort_keys=False):
    return json_serialize(data, sort_keys=sort_keys, indent=None, separators=(",", ":"))


def json_deserialize(data, ordered=True):
    if ordered:
        return json.loads(data, object_pairs_hook=collections.OrderedDict)

    return json.loads(data)


def gzipit(data):
    gzip_file = io.BytesIO()
    with gzip.GzipFile(fileobj=gzip_file, mode="wb") as f:
        f.write(data)

    return gzip_file.getvalue()


def gunzip(data):
    with gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb") as f:
        return f.read()


def file_read_utf8(filename, encoding="utf8", errors="replace"):
    return file_read_binary(filename).decode(encoding, errors).replace("\r", "")


def file_write_utf8(filename, s):
    if not isinstance(s, str):
        raise Exception("file_write_utf8 called with %s" % type_name(s))

    with io.open(filename, "wb") as of:
        of.write(s.encode("utf8"))


def file_read_binary(filename):
    filename = windows_long_path_fix(filename)

    if not os.path.isfile(filename):
        raise Exception("File %s does not exist." % quote_name(filename))

    with io.open(filename, "rb") as of:
        return of.read()


def file_write_binary(filename, data):
    if not isinstance(data, bytes):
        raise Exception("file_write_binary called with %s" % type_name(data))

    with io.open(filename, "wb") as of:
        of.write(data)


def windows_long_path_fix(filename):

    if (IS_WINDOWS and len(filename) >= 260 and isinstance(filename, str) and
            re.match("^[A-Z]:[/\\\\]", filename, flags=re.IGNORECASE) and not os.path.isfile(filename)):
        el_filename = "\\\\?\\" + filename.replace("/", "\\")
        if os.path.isfile(el_filename):
            return el_filename

    return filename


class disable_debug_log:
    def __enter__(self):
        logging.disable(logging.DEBUG)

    def __exit__(self, type, value, traceback):
        logging.disable(logging.NOTSET)


def check_abs_path(path):
    if not path.startswith("/"):
        raise Exception("check_abs_path: '%s' is not rooted" % path)

    return path


def check_rel_path(path):
    if path.startswith("/"):
        raise Exception("check_rel_path: '%s' is rooted" % path)

    return path


def unroot_path(path):
    return check_abs_path(path)[1:]


def root_path(path):
    return "/" + check_rel_path(path)


def dirname(filename):
    return check_abs_path(posixpath.dirname(check_abs_path(filename)))


def urlabspath(url, ref_from=None, working_dir=None):
    if ref_from is not None:
        working_dir = dirname(ref_from)

    purl = urllib.parse.urlparse(url, INTERNAL_FILE_SCHEME)
    if purl.scheme != INTERNAL_FILE_SCHEME or purl.netloc != "":
        return url

    return abspath(purl.path, working_dir) + ("#" + purl.fragment if purl.fragment else "")


def abspath(rel_path, working_dir):
    return check_abs_path(posixpath.normpath(posixpath.join(check_abs_path(working_dir), check_rel_path(rel_path))))


def urlrelpath(url, ref_from=None, working_dir=None, quote=True):
    if ref_from is not None:
        working_dir = dirname(ref_from)

    purl = urllib.parse.urlparse(url, INTERNAL_FILE_SCHEME)
    if purl.scheme != INTERNAL_FILE_SCHEME or purl.netloc != "":
        return url

    rp = relpath(purl.path, working_dir) + ("#" + purl.fragment if purl.fragment else "")

    return urllib.parse.quote(rp, safe="/#") if quote else rp


def relpath(abs_path, working_dir):
    return check_rel_path(posixpath.relpath(check_abs_path(abs_path), check_abs_path(working_dir)))


def get_url_filename(url):
    purl = urllib.parse.urlparse(url, INTERNAL_FILE_SCHEME)
    if purl.scheme != INTERNAL_FILE_SCHEME or purl.netloc != "":
        return None

    path = urllib.parse.unquote(purl.path)

    if not path.startswith("/"):
        return None

    return path


def root_filename(name):
    return name if name.startswith("/") else "/" + name


def windows_user_dir(local_appdata=False, appdata=False):
    if not IS_WINDOWS:
        raise Exception("Windows API is not supported on this platform")

    import ctypes.wintypes

    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", ctypes.wintypes.DWORD),
            ("Data2", ctypes.wintypes.WORD),
            ("Data3", ctypes.wintypes.WORD),
            ("Data4", ctypes.wintypes.BYTE * 8)
        ]

        def __init__(self, uuid_):
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], rest = uuid.UUID(uuid_).fields
            for i in range(2, 8):
                self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xff

    SHGetKnownFolderPath = ctypes.WINFUNCTYPE(
            ctypes.wintypes.HANDLE, ctypes.POINTER(GUID), ctypes.wintypes.DWORD, ctypes.wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p))(
            ("SHGetKnownFolderPath", ctypes.windll.shell32))

    CoTaskMemFree = ctypes.WINFUNCTYPE(None, ctypes.c_wchar_p)(("CoTaskMemFree", ctypes.windll.ole32))

    FOLDERID_RoamingAppData = "{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}"
    FOLDERID_LocalAppData = "{F1B32785-6FBA-4FCF-9D55-7B8E7F157091}"
    FOLDERID_Profile = "{5E6C858F-0E22-4760-9AFE-EA3317B67173}"
    fid = FOLDERID_LocalAppData if local_appdata else (FOLDERID_RoamingAppData if appdata else FOLDERID_Profile)

    ppath = ctypes.c_wchar_p()

    hresult = SHGetKnownFolderPath(
                ctypes.byref(GUID(fid)),
                0,
                None,
                ctypes.byref(ppath))

    if hresult:
        raise Exception("SHGetKnownFolderPath(%s) failed: %s" % (fid, windows_error(hresult)))

    path = ppath.value
    CoTaskMemFree(ppath)

    return path


def windows_error(hresult=None):
    if not IS_WINDOWS:
        raise Exception("Windows API is not supported on this platform")

    import ctypes

    if hresult is None:
        hresult = ctypes.GetLastError()

    return "%08x (%s)" % (hresult, ctypes.FormatError(hresult & 0xffff) if hresult & 0xffff0000 in [0x80070000, 0] else "?")


def wine_user_dir(local_appdata=False, appdata=False):
    raise Exception("Linux/Wine is not currently supported.")


def wineprefix():
    return os.getenv("WINEPREFIX") or os.path.join(os.getenv("HOME"), ".wine")


def winepath(path):
    return os.path.join(
        wineprefix(),
        "dosdevices",
        re.sub("[A-Z]+:", lambda x: x.group().lower(), path.replace("\\", "/"), count=1))


def wine_userreg():
    userreg = os.path.join(wineprefix(), "user.reg")
    if not os.path.isfile(userreg):
        raise Exception((
            "Wine registry file %s not found. Ensure that Wine is correctly installed and that calibre is not "
            "installed within a separate container.") % userreg)
    return userreg


def wine_arch():
    with io.open(wine_userreg(), "r") as file:
        for line in file:
            if line.startswith("#arch"):
                if "64" in line:
                    return "64"
                else:
                    return "32"


def wine_executable():
    return "wine64" if wine_arch() == "64" else "wine"


def unicode_argv(argv):
    if isinstance(argv[0], str):
        return argv

    if not IS_WINDOWS:
        return locale_decode(argv)

    import ctypes.wintypes

    GetCommandLineW = ctypes.WINFUNCTYPE(ctypes.wintypes.LPCWSTR)(
            ("GetCommandLineW", ctypes.windll.kernel32))

    CommandLineToArgvW = ctypes.WINFUNCTYPE(
            ctypes.POINTER(ctypes.wintypes.LPCWSTR), ctypes.wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int))(
            ("CommandLineToArgvW", ctypes.windll.shell32))

    cmd = GetCommandLineW()

    argc_ = ctypes.c_int(0)
    argv_ = CommandLineToArgvW(cmd, ctypes.byref(argc_))

    return [argv_[i] for i in range(argc_.value - len(argv), argc_.value)]


def locale_encode(x):
    if isinstance(x, list):
        return [locale_encode(a) for a in x]

    if isinstance(x, dict):
        return dict([(locale_encode(a), locale_encode(b)) for a, b in x.items()])

    if isinstance(x, str):
        return x.encode(LOCALE_ENCODING, errors="strict")

    return x


def locale_decode(x, encoding=LOCALE_ENCODING, silent=False):
    if isinstance(x, list):
        return [locale_decode(a, encoding, silent) for a in x]

    if isinstance(x, dict):
        return dict([(locale_decode(a, encoding, silent), locale_decode(b, encoding, silent)) for a, b in x.items()])

    if isinstance(x, bytes):
        if not silent:
            try:
                return x.decode(encoding, errors="strict")
            except UnicodeDecodeError:
                log.info("failed to decode string %s using %s" % (bytes_to_separated_hex(x), encoding))

        return x.decode(encoding, errors="replace")

    if isinstance(x, str):
        return x

    raise Exception("locale_decode does not support %s" % type_name(x))


def is_printable_ascii(data):
    for c in data:
        if c < 32 or c > 127:
            return False

    return True


def b64(s):
    return base64.b64encode(s).decode("ascii").replace("\n", "")


def user_home_dir():
    if IS_WINDOWS:
        return windows_user_dir()
    else:
        return locale_decode(os.path.expanduser("~"))


def clean_message(msg):
    return html.escape(msg, quote=False).replace("%", "%%").replace("{", "(").replace("}", ")") if msg else ""


def join_search_path(*args):
    pl = []
    for arg in args:
        if arg:
            pl.extend(arg.split(PATH_SEPARATOR))

    path_list = []
    for dir in pl:
        if dir and dir not in path_list:
            path_list.append(dir)

    return PATH_SEPARATOR.join(path_list)


def make_unique_name(root_name, check_set, sep="", always_suffix=False):
    if (not always_suffix) and root_name and root_name not in check_set:
        return root_name

    unique_number = 0
    while True:
        unique_name = "%s%s%d" % (root_name, sep, unique_number)
        if unique_name not in check_set:
            return unique_name

        unique_number += 1


class KFXDRMError(ValueError):
    pass


@functools.total_ordering
class DataFile(object):
    def __init__(self, name_or_stream, data=None, parent=None):
        if isinstance(name_or_stream, bytes):
            name_or_stream = name_or_stream.decode("utf-8")

        if isinstance(name_or_stream, str):
            self.stream = None
            self.relname = name_or_stream
            self.is_real_file = data is None
        else:
            self.stream = name_or_stream
            self.relname = self.stream.name if hasattr(self.stream, "name") else "stream"
            self.is_real_file = False

        self.data = data
        self.parent = parent

        self.name = self.relname
        self.ext = os.path.splitext(self.relname)[1]

    def get_data(self):
        if self.data is None:
            if self.stream is not None:
                self.stream.seek(0)
                self.data = self.stream.read()
                self.stream.seek(0)
            else:
                self.data = file_read_binary(self.name)

        return self.data

    def is_zipfile(self):
        return self.ext in [".azk", ".kfx-zip", ".kpf", ".zip"] or self.get_data().startswith(ZIP_SIGNATURE)

    def as_ZipFile(self):
        if self.is_real_file:
            return zipfile.ZipFile(self.name, "r")

        return zipfile.ZipFile(io.BytesIO(self.get_data()), "r")

    def relative_datafile(self, relname):

        if self.is_real_file:
            dirname = os.path.dirname(self.name)
            if dirname:
                relname = os.path.join(dirname, relname)

            if IS_WINDOWS:
                relname = relname.replace("/", "\\")

            return DataFile(relname)

        elif self.parent is not None:
            relname = relname.replace("\\", "/")
            dirname = posixpath.dirname(self.relname)
            if dirname:
                relname = posixpath.join(dirname, relname)

            with self.parent.as_ZipFile() as zf:
                return DataFile(relname, zf.read(relname), self.parent)

        else:
            raise Exception("Cannot locate file relative to unknown parent: %s" % relname)

    def __eq__(self, other):
        if not isinstance(other, DataFile):
            raise Exception("DataFile __eq__: comparing with %s" % type_name(other))

        return self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, DataFile):
            raise Exception("DataFile __lt__: comparing with %s" % type_name(other))

        return self.name < other.name


def OD(*args):
    od = collections. OrderedDict()
    for i in range(0, len(args), 2):
        od[args[i]] = args[i+1]

    return od


def md5(data):
    return hashlib.md5(data).digest()


def sha1(data):
    return hashlib.sha1(data).digest()


def sha256(data):
    return hashlib.sha256(data).digest()


ENABLE_WIDE_UNICODE_HANDLING = True

UNICODE_PYTHON_NARROW_BUILD = (sys.maxunicode < 0x10ffff)

if UNICODE_PYTHON_NARROW_BUILD and ENABLE_WIDE_UNICODE_HANDLING:
    unicode_cache = {}

    def flush_unicode_cache():
        unicode_cache.clear()

    def cache_unicode(s):
        lst = []
        i = 0
        has_surrogate = False

        while i < len(s):
            c = s[i]
            o = ord(c)
            i += 1

            if o >= 0xd800 and o <= 0xdbff and i < len(s) and ord(s[i]) >= 0xdc00 and ord(s[i]) <= 0xdfff:
                lst.append(s[i-1:i+1])
                has_surrogate = True
                i += 1
            else:
                lst.append(c)

        if not has_surrogate:
            lst = False

        unicode_cache[s] = lst
        return lst

    def unicode_len(s):
        lst = unicode_cache.get(s)
        if lst is None:
            lst = cache_unicode(s)

        if lst is False:
            return len(s)

        return len(lst)

    def unicode_slice(s, start, stop=None):
        lst = unicode_cache.get(s)
        if lst is None:
            lst = cache_unicode(s)

        if lst is False:
            return s[start:stop]

        return "".join(lst[start:stop])

else:
    def flush_unicode_cache():
        pass

    unicode_len = len

    def unicode_slice(s, start, stop=None):
        return s[start:stop]


class Serializer(object):
    def __init__(self):
        self.buffers = []
        self.length = 0

    def pack(self, fmt, *values):
        fmt_pos = (fmt, len(self.buffers))
        self.append(struct.pack(fmt, *values))
        return fmt_pos

    def repack(self, fmt_pos, *values):
        fmt, position = fmt_pos
        self.buffers[position] = struct.pack(fmt, *values)

    def append(self, buf):
        if buf:
            self.buffers.append(buf)
            self.length += len(buf)

    def extend(self, serializer):
        self.buffers.extend(serializer.buffers)
        self.length += serializer.length

    def __len__(self):
        return self.length

    def serialize(self):
        return b"".join(self.buffers)

    def sha1(self):
        sha1 = hashlib.sha1()

        for buf in self.buffers:
            sha1.update(buf)

        return sha1.digest()


class Deserializer(object):
    def __init__(self, data):
        self.buffer = data
        self.offset = 0

    def unpack(self, fmt, advance=True):
        result = struct.unpack_from(fmt, self.buffer, self.offset)[0]

        if advance:
            self.offset += struct.calcsize(fmt)

        return result

    def extract(self, size=None, upto=None, advance=True):
        if size is None:
            size = len(self) if upto is None else (upto - self.offset)

        data = self.buffer[self.offset:self.offset + size]

        if len(data) < size or size < 0:
            raise Exception("Deserializer: Insufficient data (need %d bytes, have %d bytes)" % (size, len(data)))

        if advance:
            self.offset += size

        return data

    def __len__(self):
        return len(self.buffer) - self.offset
