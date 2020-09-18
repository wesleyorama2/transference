import uuid


class Proxy():
    def __init__(self):
        self.id = uuid.uuid4()

    def run(self):
        print(self.id)
