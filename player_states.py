from state_machine import *
from settings import *

class PlayerIdleState(State):
    def __init__(self, player):
        self.player = player
        self.name = "idle"

    def get_state_name(self):
        return "idle"

    def enter(self):
        self.player.image.fill(WHITE)
        print('enter player idle state')

    def exit(self):
        print('exit player idle state')

    def update(self):
        # print('updating player idle state...')
        self.player.image.fill(WHITE)
        keys = pg.key.get_pressed()
        # if keys[pg.K_k]:
        #     print('transitioning to attack state...')
        #     self.player.state_machine.transition("attack")
            
class PlayerMoveState(State):
    def __init__(self, player):
        self.player = player
        self.name = "move"

    def get_state_name(self):
        return "move"

    def enter(self):
        self.player.image.fill(WHITE)
        print('enter player move state')

    def exit(self):
        print('exit player move state')

    def update(self):
        # print('updating player move state...')
        self.player.image.fill(GREEN)
        keys = pg.key.get_pressed()

class PlayerDashState(State):
    def __init__(self, player):
        self.player = player
        self.name = "dash"

    def get_state_name(self):
        return "dash"

    def enter(self):
        self.player.image.fill(WHITE)
        self.player.dash_rect = pg.Rect(0, 0, TILESIZE-5, TILESIZE-5)
        print('enter player move state')

    def exit(self):
        print('exit player move state')
        self.player.dash_rect = pg.Rect(0,0,0,0)

    def update(self):
        # print('updating player move state...')
        self.player.image.fill(GREEN)
        keys = pg.key.get_pressed()