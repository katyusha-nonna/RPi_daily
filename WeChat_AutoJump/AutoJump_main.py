import cv2
import math
import numpy as np
import os
import time

class AutoJump():
    def __init__(self, iterator_cont_input=100, wait_time_input=4):
        self.screencap=None
        self.distance=0
        self.jump_time=0
        self.screencap_cmd="adb shell screencap -p | sed 's/\\\\r$//' > /home/katyusha-nonna/PycharmProjects/VX_jump/adb_screen_save/screen.png"
        self.screencap_path="/home/katyusha-nonna/PycharmProjects/VX_jump/adb_screen_save/screen.png"
        self.template_path="/home/katyusha-nonna/PycharmProjects/VX_jump/template_matching/qizi.png"
        self.template=cv2.imread(self.template_path, cv2.IMREAD_GRAYSCALE)
        w, h=self.template.shape[::-1]
        self.template_w=w
        self.template_h=h
        self.distance_p=0.65
        self.direction="right"
        self.iterator_cont=iterator_cont_input  #自动跳的次数
        self.wait_time=wait_time_input
        print("初始化完毕")

    def get_screencap(self):
        print("开始截图")
        os.system(self.screencap_cmd)
        time.sleep(2)
        self.screencap=cv2.imread(self.screencap_path, cv2.IMREAD_GRAYSCALE)
        print("截图完毕")

    def clear_screencap(self):
        self.screencap=None
        self.distance=0
        self.jump_time=0
        self.direction="right"


    def get_distance(self):
        img=self.screencap.copy()
        w0, h0 = img.shape[::-1]
        res = cv2.matchTemplate(img, self.template, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        start_x, start_y = int(max_loc[0] + self.template_w / 2), max_loc[1] + self.template_h

        edges = cv2.Canny(img, 100, 200)
        for y in range(max_loc[1], max_loc[1] + self.template_h):
            for x in range(max_loc[0], max_loc[0] + self.template_w):
                edges[y][x] = 0

        center_x, center_y = 0, 0
        max_x = 0

        for y in range(600, 1200):
            for x in range(0, w0):
                if edges[y, x] == 255:
                    if center_x == 0:
                        center_x = x
                    if x > max_x:
                        center_y = y
                        max_x = x
        if center_x<540:
            self.direction="left"
            min_x=1000
            center_x, center_y = 0, 0
            for y in range(600, 1200):
                for x in range(0, w0):
                    if edges[y, x] == 255:
                        if center_x == 0:
                            center_x = x
                        if x < min_x:
                            center_y = y
                            min_x = x
        self.distance=math.sqrt(math.pow(center_x-start_x, 2)+math.pow(center_y-start_y, 2))
        print("已计算出距离：%d(单位：像素)"%self.distance)

    def distance2time(self):
        if self.direction=="right":
            self.jump_time=int(self.distance/self.distance_p)
        else:
            self.jump_time = int((self.distance / self.distance_p))
        print("已计算出跳跃时间：%d(单位：毫秒)" % self.jump_time)
        print("跳跃方向是：%s"%self.direction)
    def jump(self):
        jump_cmd = "adb shell input swipe 200 200 200 200 " + str(self.jump_time)
        os.system(jump_cmd)


    def auto_operate(self):

        for jump_cont in range(self.iterator_cont):
            print("================================================")
            self.get_screencap()
            self.get_distance()
            self.distance2time()
            self.jump()
            self.clear_screencap()
            print("================================================")
            time.sleep(self.wait_time)

if __name__=="__main__":
    test=AutoJump(10, 5)
    test.auto_operate()
    print("程序完毕")
