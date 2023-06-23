import os


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def get_extension(filename):
    return filename.rsplit(".", 1)[1].lower()


def allowed_file(filename):
    return "." in filename and get_extension(filename) in ALLOWED_EXTENSIONS


def convert(name):
    from PIL import Image

    try:
        new_name = name.rsplit(".", 1)[0] + ".png"
        Image.open(name).convert("RGB").save(new_name)

        return new_name
    except EOFError as err:
        raise err
