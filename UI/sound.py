import pyglet
import logging
import threading
import time

end = False


def ticking():
    while not end:
        time.sleep(0.1)
        pyglet.clock.tick()


def play_forever():
    player.load_audio("UI/sounds/Ambient/Ambient_all.wav", "ambient_all")
    player.play_audio("ambient_all", "main", loop=True)


class Audio:
    def __init__(self, source):
        self.source = source


class MusicPlayer:
    def __init__(self, thread):
        self.channels = {}
        self.audios = {}
        self.tickthread = thread
        thread.start()

    def load_audio(self, path, name, streaming=False):
        self.audios[name] = Audio(pyglet.resource.media(path, streaming=streaming))

    def play_audio(self, name, channel, volume=1.0, speed=1.0, loop=False):
        if name not in self.audios:
            return False
        if channel in self.channels:
            self.channels[channel].delete()

        player = pyglet.media.Player()
        player.volume = volume
        player.pitch = speed
        player.queue(self.audios[name].source)
        self.channels[channel] = player

        player.play()
        #if loop:
            #player.eos_action = pyglet.media.loop

    def stop(self):
        global end
        end = True
        for c in self.channels:
            self.channels[c].delete()


thread = threading.Thread(target=ticking)
player = MusicPlayer(thread)

if __name__ == "__main__":
    import time
    player.load_audio("sounds/Ambient/Ambient_all.wav", "ambient_all", streaming=True)
    player.load_audio("sounds/Ambient/Ambient_green.wav", "ambient_green")
    print("gonna play...")
    player.play_audio("ambient_all", "main")
    player.play_audio("ambient_green", "secondary", volume=0.5)
    print("Playing and sleping")
    #time.sleep(10)
    print("finished sleping")
