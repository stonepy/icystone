class a:
    def __init__(self):
        self.h = "hello"
        a.j(self)

    def j(self):
        print(self.h)
a()