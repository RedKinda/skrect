import game
import datetime
import redacted.misc_utilities as utils
from UI.colored_text import ColorString
import random

class ShopItem():
    def __init__(self, name=None, cost=0, amount=1):
        self.name = name
        self.cost = cost
        self.amount = amount

class CartItem():
    def __init__(self, item=None, amount=1):
        self.item=item
        self.amount=amount


class MainRoom(game.Location):
    def __init__(self, name='Main room'):
        super().__init__(name=name, description="You are in the main room of this store. You should be able to buy some food here.")

        self.cart_contents = []
        self.items = {
            'Instant noodles':ShopItem(name='Instant noodles', cost=5, amount=1),
            'Instant soup':ShopItem(name='Instant soup', cost=20, amount=3),
            'Bread':ShopItem(name='Bread', cost=8, amount=1)
        }

        self.in_stock = {self.items['Instant noodles']:0, self.items['Instant soup']:0, self.items['Bread']:0}
        self.oldseed = 0


        @self.object('shelves')
        def shelves():
            pass

        @shelves.action(name='Instant noodles', description='Add Instant noodles (5c) to your cart', time_cost=datetime.timedelta(seconds=10), energycost=game.EnergyCost.NONE, priority=10, color='yellow')
        def add_instant_noodles():
            item = self.items['Instant noodles']
            self.add_item_to_cart(item, 1)
        @shelves.action(name='Instant soup', description='Add Instant soup (20c, pack of 3) to your cart', time_cost=datetime.timedelta(seconds=10), energycost=game.EnergyCost.NONE, priority=11, color='yellow')
        def add_instant_soup():
            item = self.items['Instant soup']
            self.add_item_to_cart(item, 1)
        @shelves.action(name='Bread', description='Add Bread (8c) to your cart', time_cost=datetime.timedelta(seconds=10), energycost=game.EnergyCost.NONE, priority=12, color='yellow')
        def add_bread():
            item = self.items['Bread']
            self.add_item_to_cart(item, 1)
        @shelves.action(name='Remove Instant noodles', description='Remove Instant noodles from your cart', time_cost=datetime.timedelta(seconds=10), energycost=game.EnergyCost.NONE, priority=20, disabled=True, color='yellow')
        def remove_instant_noodles():
            item = self.items['Instant noodles']
            self.add_item_to_cart(item, -1)
        @shelves.action(name='Remove Instant soup', description='Remove Instant soup from your cart', time_cost=datetime.timedelta(seconds=10), energycost=game.EnergyCost.NONE, priority=21, disabled=True, color='yellow')
        def remove_instant_soup():
            item = self.items['Instant soup']
            self.add_item_to_cart(item, -1)
        @shelves.action(name='Remove Bread', description='Remove Bread from your cart', time_cost=datetime.timedelta(seconds=10), energycost=game.EnergyCost.NONE, priority=22, disabled=True, color='yellow')
        def remove_bread():
            item = self.items['Bread']
            self.add_item_to_cart(item, -1)

        @shelves.action(name='check cart contents', description='Check the contents of your shopping cart', time_cost=datetime.timedelta(seconds=30), energycost=game.EnergyCost.MENTAL, priority=30, color='yellow')
        def check_cart_contents():
            self.show_cart_contents(30)

        @shelves.action(name='checkout', description='Purchase the contents of your shopping cart', time_cost=datetime.timedelta(minutes=3), energycost=game.EnergyCost.LIGHT, priority=31, color='yellow')
        def checkout():
            if self.cart_contents == []:
                game.show_message("There is nothing in your cart.")
                return

            total_cost = 0
            for thing in self.cart_contents:
                total_cost += thing.item.cost*thing.amount
            money = game.game_state.get_stat('money')
            if total_cost > money:
                game.show_message('Your total is {}c. Unfortunately you do not have enough money.'.format(total_cost))
                return
            money -= total_cost
            game.game_state.set_stat('money', money)
            for thing in self.cart_contents:
                for i in range(thing.amount*thing.item.amount):
                    utils.add_to_inventory(thing.item.name)
                    self.get_object('shelves').get_action('Remove ' + thing.item.name).disable()
            game.show_message('Your total is {}c. You take the items you bought with you.'.format(total_cost))
            self.cart_contents = []


        @self.action("Work until 16", description="Work here from 8 to 16.", time_cost=datetime.timedelta(hours=8), energycost=game.EnergyCost.MENTAL, priority=40, disabled=True, color="yellow")
        def work():
            game.game_state.time = game.game_state.time.replace(hour=8, minute=0, second=0)
            game.show_message("You worked for 8 hours. You feel tired and hungry. You made 20c")
            utils.spend_money(-20)
            work.disable()

    def add_item_to_cart(self, item, amount):
        in_cart = False
        for thing in self.cart_contents:
            if thing.item == item:
                in_cart = True
                thing.amount += amount
                if thing.amount == 0:
                    self.cart_contents.remove(thing)
                    self.get_object('shelves').get_action('Remove ' + item.name).disable()
                else:
                    self.get_object('shelves').get_action('Remove ' + item.name).enable()
                break
        if not in_cart:
            self.cart_contents.append(CartItem(item))
            self.get_object('shelves').get_action('Remove ' + item.name).enable()
        self.in_stock[item] += -amount

        if self.in_stock[item]:
            self.get_object('shelves').get_action(item.name).enable()
        else:
            self.get_object('shelves').get_action(item.name).disable()

        if amount >= 0:
            game.show_message('You add the {} to your shopping cart.'.format(item.name))
        else:
            game.show_message('You remove the {} from your shopping cart.'.format(item.name))

    def show_cart_contents(self, width=30):
        if len(self.cart_contents) == 0:
            game.show_message('There is nothing in your shopping cart.')
            return
        total_cost = 0
        message = 'In your shopping cart, there is:\n'
        for thing in self.cart_contents:
            m_start = '{}× {} '.format(thing.amount, thing.item.name)
            m_end = ' {}\n'.format(thing.item.cost*thing.amount)
            message += m_start + (width - len(m_start) - len(m_end))*'.' + m_end
            total_cost += thing.item.cost*thing.amount
        m_start = 'Total: '
        m_end = ' {}\n'.format(total_cost)
        message += m_start + '_'*(width - len(m_start) - len(m_end)) + m_end
        game.show_message(message)

    def restock(self):
        seed = game.game_state.get_stat('seed')
        if seed == self.oldseed:
            return

        random.seed(a=seed)
        for thing in self.in_stock:
            self.in_stock[thing] = random.randrange(1, 16)

    def when_entering(self, from_location):
        self.restock()
        game.game_state.location = self

    def after_action(self, action):
        if job:
            if game.game_state.time.hour < 7:
                pass
            elif game.game_state.time.hour < 8:
                self.get_action("Work until 16").enable()
            elif game.game_state.time.hour < 9 and game.game_state.time.minute < 15:
                self.get_action("Work until 16").enable()


class StorageRoom(game.Location):
    def __init__(self, name='Storage room'):
        super().__init__(name=name, description="This is the storage room. Things that are not being sold are here.")

        @self.object('storage shelves')
        def storage_shelves():
            pass

        #self.get_object('storage shelves').glasses = game.Alignment.INDEPENDENT

        @storage_shelves.action('Switch glasses', time_cost=datetime.timedelta(seconds=15), energycost=game.EnergyCost.NONE, color='cyan')
        def switch_glasses():
            game.game_state.show_message(ColorString(('You put the glasses on. You leave your old ones in their place. This way you can safely see everything even in public.', 'white')))
            self.get_action("Equip Lens").disable()
            game.game_state.set_stat("fake_glass", True)
            self.get_action('Travel to Office').enable()
            self.get_object("storage shelves").get_action("Switch glasses").disable()

        @storage_shelves.action("Inspect defective glasses", time_cost=datetime.timedelta(seconds=5), energycost = game.EnergyCost.NONE)
        def inspecc_glass():
            if game.game_state.get_stat("fake_glass"):
                game.game_state.show_message(ColorString(("There are some defective glasses. ","white"),("You took one of them and left your old one in its place.","cyan")))
            else:
                game.game_state.show_message(ColorString(("There are some defective glasses. One of them have colorless lens. ","white"),("Now that you think about it, no one wearing the glasses can tell you're wearing a colorless piece.","cyan")))

        @self.action(name="Remove Lens", time_cost=datetime.timedelta(seconds=1), disabled = True, energycost=game.EnergyCost.LIGHT)
        def lens_remove():
            game.game_state.glasses.type = game.Alignment.INDEPENDENT
            self.get_action('Travel to Office').disable()
            self.get_action("Equip Lens").enable()
            self.get_action("Remove Lens").disable()
            game.game_state.show_message(ColorString(("You briefly took down your red glasses.","cyan")))

        @self.action(name="Equip Lens", time_cost=datetime.timedelta(seconds=1), energycost=game.EnergyCost.LIGHT, color = "yellow", disabled = True)
        def lens_equip():
            game.game_state.glasses.type = game.Alignment.GOVERNMENT
            self.get_action('Travel to Office').enable()
            self.get_action("Equip Lens").disable()
            self.get_action("Remove Lens").enable()
            game.game_state.show_message(ColorString(("You put your red glasses back on.","red")))

    #def glasses_off(self):
    #    self.glasses = game.game_state.glasses.type
    #    game.game_state.glasses.type = game.Alignment.INDEPENDENT
    #    self.get_action('Travel to Inconvenience store').disable()
    #    self.get_action('Equip Lens').enable()
    #    if self.glasses == game.Alignment.GOVERNMENT:
    #        self.get_action('Equip Lens').color = 'yellow'
    #    else:
    #        self.get_action('Equip Lens').color = 'white'
    #    self.get_action('Remove Lens').disable()
    #    self.get_object('storage shelves').get_action('Switch glasses').enable()

    #def glasses_on(self):
    #    game.game_state.glasses.type = self.glasses
    #    self.glasses = None
    #    self.get_action('Travel to Inconvenience store').enable()
    #    self.get_action('Remove Lens').enable()
    #    self.get_action('Equip Lens').disable()
    #    self.get_object('storage shelves').get_action('Switch glasses').disable()


    def when_entering(self, from_location):
        if not game.game_state.get_stat("fake_glass") and game.game_state.get_stat("truth"):
            self.get_action("Remove Lens").enabled = True
            game.game_state.show_message("You should be able to remove your Lens now.")
        game.game_state.location = self


class Office(game.Location):
    def __init__(self, name='Office'):
        super().__init__(name=name, description="This is the store manager's office.")

        global job
        job = False


        @self.object('manager')
        def manager():
            pass

        @manager.action('Apply for job', description='Apply for a job as a cashier', time_cost=datetime.timedelta(minutes=30), energycost=game.EnergyCost.MENTAL, color='yellow')
        def apply():
            global job

            job = True
            self.get_action('Travel to Staff room').enable()
            self.get_action("Travel to Storage room").enable()
            apply.disable()
            self.get_object("manager").get_action("Leave job").enable()
            game.show_message("The interview went well. You are hired as a cashier in the Inconvenience store.")

        @manager.action('Leave job', description='Leave your job as a cashier', disabled=True)
        def leave_job():
            global job

            job = False
            self.get_action("Travel to Staff room").disable()
            self.get_action("Travel to Storage room").disable()
            leave_job.disable()
            self.get_object("manager").get_action("Apply for job").enable()
            game.show_message("You left your position as a cashier in the Inconvenience store.")


class StaffRoom(game.Location):
    def __init__(self, name='Staff room'):
        super().__init__(name=name, description="This is the staff room. You can rest here if you need to.")

        @self.object('couch')
        def couch():
            pass

        @couch.action('Take a nap', description="Take a 30 minute nap", time_cost=datetime.timedelta(minutes=30), energycost=-1, color='white')
        def nap():
            utils.sleep(datetime.timedelta(minutes=20))
            game.show_message("You took a nice nap.")

        @self.object("kettle")
        def kettle():
            pass

        @kettle.action(name="Make Instant noodles", time_cost=datetime.timedelta(minutes=5), energycost=game.EnergyCost.NONE, disabled=True, color="yellow")
        def make_instant_noodles():
            utils.eat(self.instant_noodles)
            utils.remove_from_inventory(self.instant_noodles.name)
            game.show_message("You cook some Instant noodles and eat them. The flavoring is a little bit off.")
            self.check_cookable()

        @kettle.action(name="Make Instant soup", time_cost=datetime.timedelta(minutes=5), energycost=game.EnergyCost.NONE, disabled=True, color="yellow")
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

main_room = MainRoom()
office = Office()
storage_room = StorageRoom()
staff_room = StaffRoom()

main_room.add_neighbor(office, timecost=datetime.timedelta(minutes=1))
office.add_neighbor(storage_room, timecost=datetime.timedelta(minutes=1))
office.get_action("Travel to Storage room").disable()
office.add_neighbor(staff_room, timecost=datetime.timedelta(seconds=20))
office.get_action('Travel to Staff room').disable()
