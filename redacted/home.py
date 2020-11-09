import game
import datetime
import redacted.misc_utilities as utils
from UI.colored_text import ColorString

class Bedroom(game.Location):
    def __init__(self):
        super().__init__(description = "You are at home, in the familiar bedroom.")

        self.has_lens = True

        #@self.action(name="magic glass", description="do them agic glasss")
        #def glass():
        #    game.game_state.glasses.type = game.Alignment.INDEPENDENT

        @self.object("flag")
        def flag():
            pass

        self.flag = self.get_object("flag")
        self.flag.desc = ColorString(("Flag of the nation hangs on your wall. It is mandatory to have one. ","red"),("A simple way to support controlled population's loyalty.","cyan"))

        @flag.action(name="Observe flag", time_cost=datetime.timedelta(seconds=10), color="red")
        def observe_flag():
            game.show_message(self.flag.desc)

        @flag.action(name="Desecrate flag", time_cost=datetime.timedelta(minutes=1), color="cyan")
        def desecrate():
            game.show_message(ColorString(("You have successfully desecrated the flag. ","cyan"),("Now that you think about it, that might not have been the best idea. You hope no one sees it.","yellow")))
            self.flag.get_action("Desecrate flag").disable()
            self.flag.desc = ColorString(("Flag of the nation hangs on your wall. It is mandatory to have one. ","red"),("It has been desecrated.","cyan"))


        @self.object("bed")
        def bed():
            pass

        @bed.action(name="Relax", description="Pass some time", time_cost=datetime.timedelta(hours=1), energycost=game.EnergyCost.NONE, color = "magenta", priority = 12)
        def nap():
            game.show_message("You took a nice nap.")
            #utils.sleep()

        @bed.action(name="Sleep", description="Sleep until 7 in the morning", time_cost=datetime.timedelta(0), priority = 10, color = "white")
        def sleep():
            time = game.game_state.time
            if time.hour > 18:
                game.game_state.time = game.game_state.time + datetime.timedelta(days=1)
                game.game_state.time = game.game_state.time.replace(hour=7, minute=0, second=0)
                utils.sleep(game.game_state.time - time)
            elif time.hour < 7:
                game.game_state.time = game.game_state.time.replace(hour=7, minute=0, second=0)
                utils.sleep(game.game_state.time - time)
            else:
                game.show_message("It is no time to sleep right now.")

        @self.object("kettle")
        def kettle():
            pass

        @kettle.action(name="Make Instant noodles", time_cost=datetime.timedelta(minutes=5), energycost=game.EnergyCost.NONE, disabled=True, color="magenta")
        def make_instant_noodles():
            utils.eat(self.instant_noodles)
            utils.remove_from_inventory(self.instant_noodles.name)
            game.show_message("You cook some Instant noodles and eat them. The flavoring is a little bit off.")
            self.check_cookable()

        @kettle.action(name="Make Instant soup", time_cost=datetime.timedelta(minutes=5), energycost=game.EnergyCost.NONE, disabled=True, color="magenta")
        def make_instant_soup():
            utils.eat(self.instant_soup)
            utils.remove_from_inventory(self.instant_soup.name)
            game.show_message("You cook a cup of Instant soup. It doesn't taste amazing, but at least it's hot.")
            self.check_cookable()

        @kettle.action(name="Eat bread", time_cost=datetime.timedelta(minutes=5), energycost=game.EnergyCost.NONE, disabled=True, color="yellow")
        def make_instant_soup():
            utils.eat(self.bread)
            utils.remove_from_inventory(self.bread.name)
            game.show_message("You eat a whole loaf of bread. That's a lot of bread to eat in 5 minutes.")
            self.check_cookable()

        @self.action(name="Remove Lens", time_cost=datetime.timedelta(seconds=1), disabled = True, energycost=game.EnergyCost.LIGHT)
        def lens_remove():
            self.has_lens = False
            game.game_state.glasses.type = game.Alignment.INDEPENDENT
            game.game_state.show_message(ColorString(("You briefly took down your red glasses.","cyan")))

        @self.action(name="Equip Lens", time_cost=datetime.timedelta(seconds=1), energycost=game.EnergyCost.LIGHT, color = "yellow", disabled = True)
        def lens_equip():
            self.has_lens = True
            game.game_state.glasses.type = game.Alignment.GOVERNMENT
            game.game_state.show_message(ColorString(("You put your red glasses back on.","red")))

    def check_cookable(self):
        self.instant_noodles = utils.Food(name='Instant noodles', saturation=.25)
        if utils.is_in_inventory(self.instant_noodles.name):
            self.get_object('kettle').get_action('Make Instant noodles').enable()
        else:
            self.get_object('kettle').get_action('Make Instant noodles').disable()

        self.instant_soup = utils.Food(name='Instant soup', saturation=.3)
        if utils.is_in_inventory(self.instant_soup.name):
            self.get_object('kettle').get_action('Make Instant soup').enable()
        else:
            self.get_object('kettle').get_action('Make Instant soup').disable()

        self.bread = utils.Food(name='Bread', saturation=.4)
        if utils.is_in_inventory(self.bread.name):
            self.get_object('kettle').get_action('Eat bread').enable()
        else:
            self.get_object('kettle').get_action('Eat bread').disable()

    def when_entering(self, from_location):
        self.check_cookable()
        game.game_state.location = self

    def after_action(self, action_executed):
        lens_remove = self.get_action("Remove Lens")
        lens_equip = self.get_action("Equip Lens")
        if not game.game_state.get_stat("fake_glass"):
            if game.game_state.get_stat("truth"):
                if self.has_lens:
                    lens_remove.enabled = True
                    lens_equip.enabled = False
                else:
                    lens_remove.enabled = False
                    lens_equip.enabled = True
            else:
                lens_remove.enabled = False
                lens_equip.enabled = False
        else:
            lens_remove.enabled = False
            lens_equip.enabled = False

class Hallway(game.Location):
    def __init__(self):
        super().__init__(description = "You are in the hallway of your house.")

        @self.object("parents")
        def parents():
            pass

        @parents.action(name = "Pay rent", time_cost = datetime.timedelta(minutes=1), priority = 5, energycost = game.EnergyCost.NONE, color = "yellow")
        def pay():
            if utils.spend_money(self.rent_level):
                game.game_state.show_message("You paid your rent for this week.")
                self.last_payment = game.game_state.time.replace(hour = 0, minute = 0, second = 0)
            else:
                game.game_state.show_message("You don't have enough.")

        @parents.action(name = "Talk to parents", time_cost = datetime.timedelta(minutes=5),priority = 10, energycost = game.EnergyCost.MENTAL, color = "yellow")
        def talk_parents():
            game.game_state.show_message(ColorString(("Your rent is currently ","white"),(str(self.rent_level)+"c","yellow"),(". Don't forget you need to pay every sunday.","white")))

    def after_action(self, action_executed):
        pay = self.get_object("parents").get_action("Pay rent")
        talk = self.get_object("parents").get_action("Talk to parents")
        if game.game_state.time.hour >= 18 or game.game_state.time.hour <= 8:
            game.show_message("Your parents are here")
            talk.enable()
            if game.game_state.time.weekday() == 6 and self.last_payment != game.game_state.time.replace(hour = 0, minute = 0, second = 0):
                pay.enabled = True
            else:
                pay.enabled = False
            if self.rent_level == 40:
                from redacted.school import holder
                if holder.sadness_level > 1:
                    self.available = False
                    pay.enabled = False
                    game.game_state.show_message("Your parents know about your behavior regarding school. You are no longer welcome here.")
                elif holder.sadness_level > 0:
                    self.rent_level = 60
                    game.game_state.show_message("Your parents do not seem happy. School must've complained about you. They raised the rent.")
            elif self.rent_level == 60:
                from redacted.school import holder
                if holder.sadness_level > 1:
                    self.available = False
                    pay.enabled = False
                    game.game_state.show_message("Your parents know about your behavior regarding school. You are no longer welcome here.")
        else:
            game.show_message("There is no one here")
            pay.enabled = False
            talk.disable()

    def when_entering(self, from_location):
        if self.available:
            last_sunday = game.game_state.time - datetime.timedelta(days=(game.game_state.time.weekday()+1))
            last_sunday = last_sunday.replace(hour = 0, minute = 0, second = 0)
            if self.last_payment < last_sunday and from_location != bedroom:
                game.game_state.show_message("It is locked")
                self.available = False
            elif from_location == bedroom and bedroom.has_lens == False:
                game.game_state.show_message(ColorString(("You can't risk someone seeing you without the Lens.", "cyan")))
            else:
                game.game_state.location = self
        else:
            game.game_state.show_message("It is locked")





def init():
    global bedroom, hall
    bedroom = Bedroom()
    hall = Hallway()
    bedroom.add_neighbor(hall, timecost = datetime.timedelta(seconds=30))
    bedroom.get_action("Travel to Hallway").priority = 20
    hall.get_action("Travel to Bedroom").priority = 15


init()
def callback():
    hall.last_payment = game.game_state.time.replace(hour = 0, minute = 0, second = 0)
    hall.rent_level = 40
    hall.available = True
game.game_init(bedroom, callback)
