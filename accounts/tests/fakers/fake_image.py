from django.core.files.images import ImageFile
from factory.django import ImageField


def fake_image(**kwargs):
    filename, content = ImageField()._make_content(kwargs)
    image = ImageFile(content.file, name=filename)
    return image
