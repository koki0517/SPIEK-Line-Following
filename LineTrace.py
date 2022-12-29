from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *


hub = PrimeHub()
timer = Timer()

colorLeft = ColorSensor('B')
colorRight = ColorSensor('D')
tank = MotorPair('A','C')

Kp = 0.8
Ki = 0.08
Kd = 0.2
last_error = 0
error = 0
basic_speed = 30

count = 0
timer.reset()

def changeRGBtoHSV(rgb):
    rgb0_255 = rgb[0] * 255 / 1024, rgb[1] * 255 / 1024, rgb[2] * 255 / 1024
    # defference between max of rgb and min of it
    maxRGB, minRGB = max(rgb0_255), min(rgb0_255)

    # 最大値 - 最小値
    diff = maxRGB - minRGB

    # Hの値を計算
    if maxRGB == minRGB : hue = 0
    elif maxRGB == rgb0_255[0] : hue = 60 * ((rgb0_255[1]-rgb0_255[2])/diff)
    elif maxRGB == rgb0_255[1] : hue = 60 * ((rgb0_255[2]-rgb0_255[0])/diff) + 120
    elif maxRGB == rgb0_255[2] : hue = 60 * ((rgb0_255[0]-rgb0_255[1])/diff) + 240
    if hue < 0 : hue += 360

    # Sの値を計算
    if maxRGB != 0:
        saturation = diff / maxRGB * 100
    else:
        saturation = 0

    # Value(Brightness)
    value = maxRGB

    return hue,saturation,value

while timer.now() < 10:
    try:
        rgb_left = colorLeft.get_rgb_intensity()
        hsv_left = changeRGBtoHSV(rgb_left)
        if 150 < hsv_left[0] < 180 and hsv_left[1] > 20 and hsv_left[2] > 10:
            print('Left sensor is on green')
        rgb_right = colorRight.get_rgb_intensity()
        hsv_right = changeRGBtoHSV(rgb_right)
        if 150 < hsv_right[0] < 180 and hsv_right[1] > 20 and hsv_right[2] > 10:
            print('Right sensor is on green')
        error = (rgb_left[1] - rgb_right[1]) / 4.7
    except:
        print('cannot get RGB')
    u = Kp * error + Ki * (error + last_error) + Kd * (error - last_error)
    tank.start_tank(int(basic_speed + u),int(basic_speed - u))
    count += 1

tank.stop()
print(count)
