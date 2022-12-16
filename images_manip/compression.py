import base64
import io
import zlib
import bz2
import gzip
from PIL import Image


class Compression:
    def __init__(self, image):
        self.image = image

    def convert(self):
        im = Image.open(self.image)
        stream = io.BytesIO()
        im.save(stream, "webp")
        data = stream.getvalue()
        return data

    def get_base64(self):
        return base64.b64encode(self.convert())

    def get_zlib(self):
        im_data = self.convert()
        im_data_compressed = zlib.compress(im_data)
        return base64.b64encode(im_data_compressed)

    def get_bz2(self):
        im_data = self.convert()
        im_data_compressed = bz2.compress(im_data)
        return base64.b64encode(im_data_compressed)

    def get_gzip(self):
        im_data = self.convert()
        im_data_compressed = gzip.compress(im_data)
        return base64.b64encode(im_data_compressed)





