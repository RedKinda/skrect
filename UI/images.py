from PIL import Image
import threading


def show_map(path="UI/images/peasant.jpg"):
    im = Image.open(path)
    threading.Thread(target=im.show).start()


if __name__ == "__main__":
    show_map("images/peasant.jpg")