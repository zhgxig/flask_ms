import os
import uuid
from urllib.parse import quote

from .orm import db
from datetime import datetime
import cropresize2
from PIL import Image
from flask import abort, request
import short_url
from werkzeug.utils import cached_property
from flask_example.utils.mimes import *
from flask_example.utils.utils import get_file_md5, get_file_path


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name


class PasteFile(db.Model):
    __tablename__ = "paste_file"
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(5000), nullable=True)
    file_hash = db.Column(db.String(128), nullable=True, unique=True)
    file_md5 = db.Column(db.String(128), nullable=True, unique=True)
    upload_time = db.Column(db.DateTime, nullable=True)
    mime_type = db.Column(db.String(256), nullable=True)
    size = db.Column(db.Integer, nullable=True)

    def __init__(self, file_name="", mime_type="application/octet-stream", size=0, file_hash=None, file_md5=None):
        self.upload_time = datetime.now()
        self.mime_type = mime_type
        self.size = int(size)
        self.file_hash = file_hash if file_hash else self._hash_file_name(file_name)
        self.file_name = file_name if file_name else self.file_hash
        self.file_md5 = file_md5

    @staticmethod
    def _hash_file_name(file_name):
        _, _, suffix = file_name.rpartition(".")
        return "%s.%s" % (uuid.uuid4().hex, suffix)

    @classmethod
    def get_by_md5(cls, file_md5):
        return cls.query.filter_by(file_md5=file_md5).first()

    @property
    def path(self):
        return get_file_path(self.file_hash)

    @classmethod
    def create_by_old_paste(cls, file_hash):
        filepath = get_file_path(file_hash)
        mimetype = magic.from_file(filepath, mime=True)
        filestat = os.stat(filepath)
        size = filestat.st_size

        rst = cls(file_hash, mimetype, size, file_hash=file_hash)
        return rst

    @classmethod
    def create_by_upload_file(cls, uploaded_file):
        rst = cls(uploaded_file.filename, uploaded_file.mimetype, 0)
        uploaded_file.save(rst.path)
        with open(rst.path, "rb") as f:
            file_md5 = get_file_md5(f)
            uploaded_file = cls.get_by_md5(file_md5)
            if uploaded_file:
                os.remove(rst.path)
                return uploaded_file

        filestat = os.stat(rst.path)
        rst.size = filestat.st_size
        rst.file_md5 = file_md5
        return rst

    @classmethod
    def rsize(cls, old_paste, weight, height):
        assert old_paste.is_image, TypeError("Unsupported Image Type")

        img = cropresize2.crop_resize(Imagea.open(old_paste.path), (int(weight), int(height)))

        rst = cls(old_paste.filename, old_paste.mimetype, 0)
        img.save(rst.path)
        filestat = os.stat(rst.path)
        rst.size = filestat.st_size
        return rst

    @classmethod
    def get_by_file_hash(cls, file_hash, code=404):
        return cls.query.filter_by(file_hash=file_hash).first() or abort(code)

    def get_url(self, subtype, is_symlink=False):
        hash_or_link = self.symlink if is_symlink else self.file_hash
        return 'http://{host}/{subtype}/{hash_or_link}'.format(subtype=subtype, host=request.host,
                                                               hash_or_link=hash_or_link)

    @property
    def url_i(self):
        return self.get_url("i")

    @property
    def url_p(self):
        return self.get_url("p")

    @property
    def url_s(self):
        return self.get_url("s", is_symlink=True)

    @property
    def url_d(self):
        return self.get_url("d")

    @cached_property
    def symlink(self):
        return short_url.encode_url(self.id)

    @classmethod
    def get_by_symlink(cls, symlink, code=404):
        id = short_url.decode_url(symlink)
        return cls.query.filter_by(id=id).first() or abort(code)

    @property
    def image_size(self):
        if self.is_image:
            f = open(self.path, 'rb')
            im = Image.open(f)
            return im.size
        return (0, 0)

    @property
    def quoteurl(self):
        return quote(self.url_i)

    @property
    def is_image(self):
        return self.mimetype in IMAGE_MIMES

    @property
    def is_audio(self):
        return self.mimetype in AUDIO_MIMES

    @property
    def is_video(self):
        return self.mimetype in VIDEO_MIMES

    @property
    def is_pdf(self):
        return self.mimetype == 'application/pdf'

    @property
    def type(self):
        for t in ('image', 'pdf', 'video', 'audio'):
            if getattr(self, 'is_' + t):
                return t

        return 'binary'
