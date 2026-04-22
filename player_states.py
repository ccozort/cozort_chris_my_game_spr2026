from state_machine import *
from settings import *
from utils import *

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
        self.player.image.fill(GREEN)
        print('enter player move state')

    def exit(self):
        print('exit player move state')

    def update(self):
        # print('updating player move state...')
        self.player.image.fill(GREEN)

class PlayerDashState(State):
    def __init__(self, player):
        self.player = player
        self.name = "dash"
        self.dash_cd = Cooldown(500)

    def get_state_name(self):
        return "dash"

    def enter(self):
        # start dash timer
        # increase speed
        # self.player.keys_enabled = False
        self.dash_cd.start()
        self.player.image.fill(RED)
        self.player.speed = PLAYER_SPEED * 3    
        self.player.dash_rect = pg.Rect(0, 0, TILESIZE-5, TILESIZE-5)
        print('enter player dash state')

    def exit(self):
        print('exit player dash state')
        self.player.dash_rect = pg.Rect(0,0,0,0)
        self.player.speed = PLAYER_SPEED
        # self.player.keys_enabled = True
    def update(self):
        self.player.effects_trail()
        print('updating player dash state...')
        # when start timer done, exit state
        self.player.image.fill(RED)
        if self.dash_cd.ready():
            print('dash done')
            self.player.state_machine.transition("idle")
        keys = pg.key.get_pressed()