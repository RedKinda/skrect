import pyglet
import logging
import threading
import time
import game

end = False


def ticking():
    while not end:
        time.sleep(0.1)
        pyglet.clock.tick()

        try:
            inf = game.game_state.get_stat("infection")
            if game.game_state.glasses.type == game.Alignment.INDEPENDENT:
                player.set_volume("all", 1 - inf)
                player.set_volume("red", 0)
            elif game.game_state.glasses.type == game.Alignment.GOVERNMENT:
                player.set_volume("all", 0)
                player.set_volume("red", 1 - inf)
            player.set_volume("green", inf)
        except:
            pass


def play_forever():
    threading.Thread(target=_play_forever).start()
    print("Spooky groove playing...")


def _play_forever():
    player.load_audio("UI/sounds/Ambient/Ambient_all.wav", "a_all")
    player.load_audio("UI/sounds/Ambient/Ambient_green.wav", "a_green")
    player.load_audio("UI/sounds/Ambient/Ambient_red.wav", "a_red")
    while True:
        player.play_audio("a_all", "all", loop=True)
        player.play_audio("a_green", "green", loop=True)
        player.play_audio("a_red", "red", loop=True)
        t = 0
        while t < 125 and not end:
            time.sleep(1)
            t += 1
        if end:
            return
        player.channels["all"].delete()
        player.channels["green"].delete()
        player.channels["red"].delete()



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
        src = self.audios[name].source

        if loop:
            looper = pyglet.media.SourceGroup()
            looper.add(src)
            player.queue(looper)
            player.loop = True
            player.on_eos = lambda: player.queue(src)
        else:
            player.queue(src)
        self.channels[channel] = player

        player.play()

    def stop(self):
        global end
        end = True
        for c in self.channels:
            self.channels[c].delete()

    def set_volume(self, channel, volume):
        self.channels[channel].volume = volume


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
