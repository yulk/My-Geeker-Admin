from flask import Flask
from flask_uploads import configure_uploads
from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)
excels = UploadSet('excels', ('xls', 'xlsx'))
words = UploadSet('words', ('doc', 'docx'))


def init_upload(app: Flask):
    configure_uploads(app, photos)
    configure_uploads(app, excels)
    configure_uploads(app, words)
