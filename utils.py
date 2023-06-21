import os


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def convert(name):
    from PIL import Image

    try:
        new_name = os.path.join("./temp/", name.rsplit(".", 1)[0] + ".png")
        Image.open(os.path.join("./temp/", name)).convert("RGB").save(new_name)

        return new_name
    except EOFError as err:
        raise err
