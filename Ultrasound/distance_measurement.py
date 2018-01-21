import RPi.GPIO as GPIO
import time

Trig_Pin=20
Echo_Pin=21  #Echo(回声)是输出引脚，输出矩形窗高电平，即声波来回时间
             #Trig(触发)是输入引脚，输入一个至少10us的触发信号，HC-SR04模块工作
GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig_Pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)

time.sleep(2)   #等待设置完成

def checkdist():
    GPIO.output(Trig_Pin, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Trig_Pin, GPIO.LOW)
    while not GPIO.input(Echo_Pin):
        pass
    t1 = time.time()
    while GPIO.input(Echo_Pin):
        pass
    t2 = time.time()
    return (t2-t1) *340/2

try:
    while True:
        print('Distance:%0.2f m' % checkdist())
        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
