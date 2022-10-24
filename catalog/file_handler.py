from PIL import Image
from pathlib import Path
from django.conf import settings
import os
import mimetypes

def handle_uploaded_cover(f, uid, title, author):
    try:
        path = Path(settings.MEDIA_ROOT / f'data/{uid}/')
        os.makedirs(path, exist_ok=True)
        with open(path / f'cover.jpg', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        image = Image.open(path / f'cover.jpg')
        width, height = image.size
        if width != 1400 or height != 2100:
            return False
        new_image = image.resize((280, 420))
        new_image.save(path / f'cover-min.jpg')

        update_cover_title(uid, title, author)
        return True
    except:
        return False


def handle_uploaded_ebook(f, uid):
    try:
        path = Path(settings.MEDIA_ROOT / f'data/{uid}/')
        os.makedirs(path, exist_ok=True)
        with open(path / f'book{uid}.epub', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True
    except:
        return False


def update_cover_title(uid, title, author):
    path = Path(settings.MEDIA_ROOT / f'data/{uid}/')
    with open(settings.MEDIA_ROOT / 'data/sample.svg', 'r') as svg:
        xml = svg.read()
        xml = xml.replace('TITLE', title).replace('AUTHOR', author)
        with open(path / 'cover.svg', 'w+') as new_svg:
            new_svg.write(xml)