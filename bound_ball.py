
import pygame
from pygame.locals import *
import sys
import math
import random

def main():
    #初期化
    pygame.init() 
    #ウィンドウサイズ
    window_x=1280
    window_y=720
    screen = pygame.display.set_mode((window_x, window_y)) # ウィンドウサイズの指定
    pygame.display.set_caption('斜方投射') # ウィンドウタイトルの指定
    font = pygame.font.Font(None, 55) 
       
    #ボール位置初期化
    ball_x=random.randint(20,1260)
    ball_y=random.randint(20,200)
    
    rect_width=200#的の幅
    rect_height=5#的の高さ
    #的の位置(左上)
    rect_x=0#random.randint(v0,window_x-rect_width)
    rect_y=window_y-rect_height
      
    point=0
    
    rand=random.randint(0,3)
    if rand==0:
        ball_x_direction=1
        ball_y_direction=1
    elif rand==1:
        ball_x_direction=-1
        ball_y_direction=1
    elif rand==2:
        ball_x_direction=1
        ball_y_direction=-1
    elif rand==3:
        ball_x_direction=-1
        ball_y_direction=-1
    
    spped=10
    
    while(True):
        screen.fill((0, 0, 0, 0))  # 画面の背景色
        pygame.time.wait(30)        # 更新時間間隔
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LEFT]:
            rect_x-=20
        if pressed_key[K_RIGHT]:
            rect_x+=20
        if rect_x<0:
            rect_x=0
        if rect_x>window_x-rect_width:
            rect_x=window_x-rect_width
                
        ball_x+=spped*ball_x_direction
        ball_y+=spped*ball_y_direction
        
        if ball_x>rect_x and ball_x<rect_x+rect_width and ball_y>window_y:
            ball_y_direction*=-1
            point+=1
        elif (ball_y>window_y):
            #ボール位置初期化
            ball_x=random.randint(20,700)
            ball_y=random.randint(20,200)
        if(ball_x<0):
            ball_x_direction*=-1
        if(ball_x>window_x):
            ball_x_direction*=-1
        if(ball_y<0):
            ball_y_direction*=-1
        
        ball_x_next=ball_x+spped*ball_x_direction
        ball_y_next=ball_y+spped*ball_y_direction
        
        angle=math.atan2(ball_y-ball_y_next,ball_x_next-ball_x)*(180/3.14)
        print(angle)
        
        pygame.draw.rect(screen, (255,0,0), (rect_x,rect_y,rect_width,rect_height))#的の描画
        pygame.draw.circle(screen, (0,95,0), (ball_x,ball_y), 10, width=0)#ボールの描画
        pygame.draw.aaline(screen, (255,0,255), (ball_x,ball_y), (ball_x_next,ball_y_next), 0)#バーの描画
        text = font.render('Score:'+str(point), True, (255,255,255))   # 描画する文字列の設定
        screen.blit(text, [10, 10])# 文字列の表示位置
        pygame.display.update()#画面更新
            
        for event in pygame.event.get():#終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
