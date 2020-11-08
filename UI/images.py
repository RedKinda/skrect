import platform
if platform.system() == "Linux":
    from PIL import Image
elif platform.system() == "Windows":
    from PIL import Image
else:
    print("Unsupported OS")
    raise OSError
import threading


def show_map(path="UI/images/mapa.png"):
    im = Image.open(path)
    threading.Thread(target=im.show).start()

'''
if __name__ == "__main__":
    show_map("images/peasant.jpg")
'''
