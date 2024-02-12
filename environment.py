import gym
import numpy as np
import pygame
import math
import random

class MyEnv(gym.Env):
    def __init__(self):
        
        #初期化
        pygame.init() 
        #ウィンドウサイズ
        self.window_x=1280
        self.window_y=720
        
        screen = pygame.display.set_mode((self.window_x, self.window_y)) # ウィンドウサイズの指定
        pygame.display.set_caption('反射球') # ウィンドウタイトルの指定
        font = pygame.font.Font(None, 55) 
        
        self.rect_width=150#プレーヤーの幅
        self.rect_height=5#プレーヤーの高さ
         
        self.spped=10#球のスピード
        
        # アクション数定義
        ACTION_NUM=3 #アクションの数が3つの場合
        self.action_space = gym.spaces.Discrete(ACTION_NUM) 
        
        # 状態の範囲を定義
        LOW = np.array([0,0,0,-135.06847396007072])
        HIGH = np.array([self.window_x,self.window_y,self.window_x-self.rect_width,135.06847396007072])
        self.observation_space = gym.spaces.Box(low=LOW, high=HIGH)
        
        self.reset()
       
    def reset(self):
        #ボール位置初期化
        self.ball_x=random.randint(20,1260)
        self.ball_y=random.randint(20,200)
        
        #球の進む方向をランダムで決める
        rand=random.randint(0,3)
        if rand==0:
            self.ball_x_direction=1
            self.ball_y_direction=1
        elif rand==1:
            self.ball_x_direction=-1
            self.ball_y_direction=1
        elif rand==2:
            self.ball_x_direction=1
            self.ball_y_direction=-1
        elif rand==3:
            self.ball_x_direction=-1
            self.ball_y_direction=-1
        
        #プレーヤーの位置
        self.rect_x=10
        self.rect_y=self.window_y-self.rect_height
        
        #ボールが次に進む位置
        self.ball_x_next=self.ball_x+self.spped*self.ball_x_direction
        self.ball_y_next=self.ball_y+self.spped*self.ball_y_direction
        
        #ボールの角度
        self.angle=math.atan2(self.ball_y-self.ball_y_next,self.ball_x_next-self.ball_x)*(180/3.14)
        
        observation=[self.ball_x,self.ball_y,self.rect_x,self.angle]
        
        return observation

    def step(self, action_index):
        done=False
        #アクションによってプレーヤーを移動する
        if action_index==0:
            self.rect_x-=20
        if action_index==1:
            self.rect_x+=20
        if self.rect_x<0:
            self.rect_x=0
        if self.rect_x>self.window_x-self.rect_width:
            self.rect_x=self.window_x-self.rect_width
        
        #ボール位置計算
        self.ball_x+=self.spped*self.ball_x_direction
        self.ball_y+=self.spped*self.ball_y_direction
        
        #ボールがプレーヤに当たったら反転
        if self.ball_x>self.rect_x and self.ball_x<self.rect_x+self.rect_width and self.ball_y>self.window_y:
            self.ball_y_direction*=-1    
        elif (self.ball_y>self.window_y):#ボールがプレーヤに当たらずに画面下に当たったら終了フラグ
            done=True
            
        #画面端に当たったら反転
        if(self.ball_x<0):
            self.ball_x_direction*=-1
        if(self.ball_x>self.window_x):
            self.ball_x_direction*=-1
        if(self.ball_y<0):
            self.ball_y_direction*=-1
        
        #ボールが次に進む位置
        self.ball_x_next=self.ball_x+self.spped*self.ball_x_direction
        self.ball_y_next=self.ball_y+self.spped*self.ball_y_direction
        
        #ボールの角度
        self.angle=math.atan2(self.ball_y-self.ball_y_next,self.ball_x_next-self.ball_x)*(180/3.14)
        
        #状態の保存
        observation=[self.ball_x,self.ball_y,self.rect_x,self.angle]
        
        #ゲームが続くと報酬
        reward=1
        return observation, reward, done, {}

    def render(self,mode):
        screen = pygame.display.set_mode((self.window_x, self.window_y)) # ウィンドウサイズの指定
        pygame.time.wait(20)#更新時間間隔
        pygame.display.set_caption("Pygame Test") # ウィンドウの上の方に出てくるアレの指定
        screen.fill((0,0,0,)) # 背景色の指定。RGBだと思う
        
        pygame.draw.rect(screen, (255,0,0), (self.rect_x,self.rect_y,self.rect_width,self.rect_height))#的の描画
        pygame.draw.circle(screen, (0,95,0), (self.ball_x,self.ball_y), 10, width=0)#ボールの描画
        pygame.draw.aaline(screen, (255,0,255), (self.ball_x,self.ball_y), (self.ball_x_next,self.ball_y_next), 0)#バーの描画
        pygame.display.update() # 画面更新
    
    def close(self):
        pygame.quit()

