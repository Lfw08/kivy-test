from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, BooleanProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import random
import time

winner_point = 5
global win

win = False


class PongPaddle(Widget):
    score = NumericProperty(0)
    score1 = StringProperty(str(score)) 
    win = False

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * random.choice([1.2,1.5,1.7])
            ball.velocity = vel.x, vel.y + random.randint(-1,1)

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    win = BooleanProperty(False)



    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self,dt):
        self.player1.score1 = str(self.player1.score)
        self.player2.score1 = str(self.player2.score)

        if self.win:
            time.sleep(3)
            self.win = False
        

        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1


        # went off to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            if self.player2.score == winner_point:
                self.player2.score1 = "Winner!"
                self.win = True
                #wait 3 seconds and restart the game
                
                self.player1.score = 0
                self.player2.score = 0
            if self.player1.score == winner_point:
                self.player1.score1 = "Winner!"
                self.win = True
                #wait 3 seconds and restart the game
                
                self.player1.score = 0
                self.player2.score = 0
            self.serve_ball(vel=(random.randint(4,6), 0))

        if self.ball.right > self.width:
            self.player1.score += 1

            if self.player2.score == winner_point:
                self.player2.score1 = "Winner!"
                self.win = True
                #wait 3 seconds and restart the game
                
                self.player1.score = 0
                self.player2.score = 0
            if self.player1.score == winner_point:
                self.player1.score1 = "Winner!"
                self.win=True
                #wait 3 seconds and restart the game
                
                self.player1.score = 0
                self.player2.score = 0

            self.serve_ball(vel=(random.randint(-6,-4), 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
