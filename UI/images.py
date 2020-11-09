
from PIL import Image
'''import platform
if platform.system() == "Linux":
elif platform.system() == "Windows":
    from PIL import Image
else:
    print("Unsupported OS")
    raise OSError'''
import threading


def show_map(path=None):
    path = path or "UI/images" + "/mapa.png"
    im = Image.open(path)
    threading.Thread(target=im.show).start()


#show_map()
'''
if __name__ == "__main__":
    show_map("images/peasant.jpg")
'''
