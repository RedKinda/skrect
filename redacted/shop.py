import game
import datetime
import redacted.misc_utilities

class ShopItem():
    def __init__(self, name=None, cost=0, amount=1):
        self.name = name
        self.cost = cost
        self.amount = amount

class CartItem():
    def __init__(self, item=None, amount=1):
        self.item=item
        self.amount=amount

class Mainroom(game.Location):
    def __init__(self):
        super().__init__()

        self.cart_contents = []
        self.items = {'instant noodles':ShopItem(name='instant noodles', cost=5, amount=1),
        'instant soup':ShopItem(name='instant soup', cost=20, amount=3),
        'bread':ShopItem(name='bread', cost=8, amount=1)}
        self.in_stock = {self.items['instant noodles']:1, self.items['instant soup']:69, self.items['bread']:1}


        @self.object('shelves')
        def shelves():
            pass

        @shelves.action(name='instant noodles', description='Add instant noodles (5c) to your cart', priority=10)
        def add_instant_noodles():
            item = self.items['instant noodles']
            self.add_item_to_cart(item, 1)
        @shelves.action(name='instant soup', description='Add instant soup (20c, pack of 3) to your cart', priority=11)
        def add_instant_soup():
            item = self.items['instant soup']
            self.add_item_to_cart(item, 1)
        @shelves.action(name='bread', description='Add bread (8c) to your cart', priority=12)
        def add_bread():
            item = self.items['bread']
            self.add_item_to_cart(item, 1)
        @shelves.action(name='remove instant noodles', description='Remove instant noodles from your cart', priority=20, disabled=True)
        def add_instant_noodles():
            item = self.items['instant noodles']
            self.add_item_to_cart(item, -1)
        @shelves.action(name='remove instant soup', description='Add instant soup to your cart', priority=21, disabled=True)
        def add_instant_soup():
            item = self.items['instant soup']
            self.add_item_to_cart(item, -1)
        @shelves.action(name='remove bread', description='Add bread to your cart', priority=22, disabled=True)
        def add_bread():
            item = self.items['bread']
            self.add_item_to_cart(item, -1)

        @self.action(name='check cart contents', description='Check the contents of your shopping cart', priority=30)
        def check_cart_contents():
            self.show_cart_contents(30)

        @self.action(name='checkout', description='Purchase the contents of your shopping cart', priority=31)
        def checkout():
            total_cost = 0
            for thing in cart_contents:
                total_cost += thing.item.cost*thing.amount
            game.show_message('Your total is {}c. Money and items not yet supported.'.format(total_cost))

    def add_item_to_cart(self, item, amount):
        in_cart = False
        for thing in self.cart_contents:
            if thing.item == item:
                in_cart = True
                thing.amount += amount
                if thing.amount == 0:
                    self.cart_contents.remove(thing)
                    self.get_object('shelves').get_action('remove ' + item.name).enabled = False
                else:
                    self.get_object('shelves').get_action('remove ' + item.name).enabled = True
                break
        if not in_cart:
            self.cart_contents.append(CartItem(item))
        self.in_stock[item] += -amount
        self.get_object('shelves').get_action('remove ' + item.name).enabled = True

        if self.in_stock[item]:
            self.get_object('shelves').get_action(item.name).enabled = True
        else:
            self.get_object('shelves').get_action(item.name).enabled = False

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

class Office(game.Location):
    def __init__(self):
        super().__init__()

        self.job = False


        @self.object('manager')
        def manager():
            pass

        @manager.action('apply', description='Apply for a job as a cashier', time_cost=datetime.timedelta(minutes=30))
        def apply():
            self.job=True
            manager.get_action('apply').enabled = False


def run():
    main = Mainroom()
    office = Office()

    main.add_neighbor(office, timecost=datetime.timedelta(minutes=2))

    def callback():
        pass

    game.game_init(main, callback)
