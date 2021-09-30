from asyncio import Queue


class Shared:
    def __init__(self):
        self.shutdown = False
        self.queue = Queue()
