from PIL import Image
import threading


def show_map(path="UI/images/mapa.png"):
    im = Image.open(path)
    threading.Thread(target=im.show).start()


if __name__ == "__main__":
    show_map("images/peasant.jpg")