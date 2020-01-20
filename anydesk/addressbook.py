class Addressbook:
    def __init__(self, api, id, name):
        self.api = api
        self.id = id
        self.name = name

    def __str__(self):
        return self.name + " (" +  str(self.id) + ")"

    def row(self):
        return [
            self.id,
            self.name
        ]
