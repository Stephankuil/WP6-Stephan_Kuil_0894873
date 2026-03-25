class Engine:
    def __init__(self, game):
        self.game = game
        self.running = True

    def run(self):
        while self.running:
            self.game.handle_events()
            self.game.update()
            self.game.render()

    def pauze(self):
        self.running = False

    def hervat(self):
        self.running = True

    def stop(self):
        self.running = False