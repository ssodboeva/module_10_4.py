import random
import time
from threading import Thread
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest (Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        wait_time = random.randint(3, 10)
        time.sleep(wait_time)


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests:
            assigned_table = None
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    assigned_table = table
                    break
            if assigned_table:
                print(f'{guest.name} сел(-а) за стол номер {assigned_table.number}')
                guest.start()
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty():
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-ф) и ушел(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None

                    if not self.queue.empty():
                        guest = self.queue.get()
                        table.guest = guest
                        print(f'{guest.name} вышел(-ла) из очереди и села(-а) за стол номер {table.number}')
                        guest.start()

tables = [Table(number) for number in range(1, 6)]

guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

guests = [Guest(name) for name in guests_names]

cafe = Cafe(*tables)

cafe.guest_arrival(*guests)

cafe.discuss_guests()
