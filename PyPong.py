# Created by Jet
# Original Git Repo: https://github.com/Jet132/PyPong
# Do not remove this Credit
#=====================================================

import random

randomBool = lambda :bool(random.getrandbits(1))

ACTION_NAMES = ["up","down","nothing"]
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_NOTHING = 2

class PyPong():


    @property
    def states(self):
        return dict(shape=(6,), type='float')

    @property
    def actions(self):
        return dict(num_actions=len(ACTION_NAMES), type='int')

    def _rand_v_dir(self,velocity):
        return (velocity if randomBool() else -velocity)

    def __init__(self, player_size=40,player_speed=8, field_size=(300,200), ball_size=10, max_score=10, start_velocity=4):
        """
        Enviroment for Pong
        requires two agent inputs
        Args:
            player_size: player height
            player_speed: player movement speed
            field_size: size of play field
            ball_size: ball size
            max_score: max score before terminal equals true
            start_velocity: velocity of ball in x direction
        """
        self.player_size = player_size
        self.player_speed = player_speed
        self.field_size = field_size
        self.ball_size = ball_size
        self.max_score = max_score
        self.ball_base_v = start_velocity

        middle_y = (int) (self.field_size[1]/2)
        self.player0 = middle_y
        self.player1 = middle_y
        self.ball = [(int) (field_size[0]/2),middle_y]
        self.ball_v = [self._rand_v_dir(start_velocity),0]
        self.scores = [0,0]

    def getRawState(self):
        """
        Returns:
            raw state (player0 y location, player1 y loc), ball loc(tuple), ball velocity(tuple).
        """
        return (self.player0,self.player1), self.ball, self.ball_v

    def getScores(self):
        """
        Returns:
            current score as array.
        """
        return self.scores

    def _pack_data(self):
        p0 = [-1,self.player0]
        p0.extend(self.ball)
        p0.extend(self.ball_v)

        p1 = [1,self.player1]
        p1.extend(self.ball)
        p1.extend(self.ball_v)

        return p0, p1

    def reset(self):
        """
        Reset environment and setup for new episode.
        Returns:
            initial states of reset environment.
        """

        middle_y = (int) (self.field_size[1]/2)
        self.player0 = middle_y
        self.player1 = middle_y
        self.ball = [(int) (self.field_size[0]/2),middle_y]
        self.ball_v = [self._rand_v_dir(self.ball_base_v),0]
        self.scores = [0,0]
        return self._pack_data()

    def _soft_reset(self):
        self.ball = [(int) (self.field_size[0]/2),(int) (self.field_size[1]/2)]
        self.ball_v = [self._rand_v_dir(self.ball_base_v),0]

    def _do_action(self,action, player_id):
        player = (self.player0 if player_id==0 else self.player1)
        player_v = 0
        if(action == ACTION_UP):
            if(player-self.player_speed>=0):
                player_v = -self.player_speed
            else:
                return False
        elif(action == ACTION_DOWN):
            if(player+self.player_size+self.player_speed<=self.field_size[1]):
                player_v = self.player_speed
            else:
                return False
        elif(action == ACTION_NOTHING):
            return True
        else:
            raise ValueError("Illegal action: {} from player {}".format(action,player_id))
        
        if(player_id == 0):
            self.player0 += player_v
        elif(player_id == 1):
            self.player1 += player_v
        else:
            raise ValueError("player_id must be either 0 or 1 but was {}".format(player_id))
        
        return True

    def _y_distance_to_ball(self, player):
        return ((player+(int)(self.player_size/2)) - self.ball[1]+(int)(self.ball_size/2))

    def _flip_side(self, side):
        return (0 if side == 1 else 1)

    def _player_catch(self, player_id):
        player = (self.player0 if player_id == 0 else self.player1)
        reward = 0
        if(self.ball[1]+self.ball_size >= player and self.ball[1] <= player+self.player_size):
            self.ball_v[0] = -self.ball_v[0]
            self.ball_v[1] = self.ball_v[1] - self._y_distance_to_ball(player) * 0.1
            reward += 50 + abs(self._y_distance_to_ball(player))
        else:
            self.scores[self._flip_side(player_id)] += 1
            reward -= 10 + abs(self._y_distance_to_ball(player))
            self._soft_reset()
        return reward

    def execute(self, action0, action1):
        """
        Executes action, observes next state(s) and reward.
        Args:
            action0/action1: Actions to execute.
        Returns:
            Tuple of ((state0, state1), (reward0, reward1),bool indicating terminal)
        """

        reward0 = 0
        reward1 = 0

        if not self._do_action(action0,0):
            #optional illegal action penalty
            pass
        if not self._do_action(action1,1):
            #optional illegal action penalty
            pass

        self.ball[0] += self.ball_v[0]
        self.ball[1] += self.ball_v[1]

        if(self.ball[0] <= 0):
            reward0 += self._player_catch(0)
        elif(self.ball[0]+self.ball_size >= self.field_size[0]):
            reward1 += self._player_catch(1)

        if(self.ball[1] < 0 or self.ball[1]+self.ball_size>self.field_size[1]):
            self.ball_v[1] = -self.ball_v[1]

        terminal = False
        if 10 in self.scores:
            terminal = True

        return self._pack_data(), (reward0,reward1), terminal
        
    def close(self):
        pass
    