from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()
timer = Timer()

colorLeft = ColorSensor('B')
colorRight = ColorSensor('D')

tank = MotorPair('A','C')
tank.set_stop_action('hold')

motorLeft = Motor('A')
motorRight = Motor('C')

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
    maxRGB, minRGB = max(rgb0_255), min(rgb0_255)

    diff = maxRGB - minRGB

    # Hue
    if maxRGB == minRGB : hue = 0
    elif maxRGB == rgb0_255[0]:
        hue = 60 * ((rgb0_255[1] - rgb0_255[2]) / diff)
    elif maxRGB == rgb0_255[1]:
        hue = 60 * ((rgb0_255[2] - rgb0_255[0]) / diff) + 120
    elif maxRGB == rgb0_255[2]:
        hue = 60 * ((rgb0_255[0] - rgb0_255[1]) / diff) + 240
    if hue < 0:
        hue += 360

    # Saturation
    if maxRGB != 0:
        saturation = diff / maxRGB * 100
    else:
        saturation = 0

    # Value(Brightness)
    value = maxRGB

    return hue,saturation,value

def green_intersection(direction):
    tank.stop()
    if direftion == "l":
        deg_start = motorLeft.get_degrees_counted()
        isRightGreen = False
        while abs(motorLeft.get_degrees_counted()) <= abs(deg_start) + 50:
            tank.start_tank(30,30)
            if isGreen('r'):
                isRightGreen = True
        tank.stop()
        if isRightGreen:
            u_turn()
        else:
            print('turn left')
    else:
        deg_start = motorRight.get_degrees_counted()
        isLeftGreen = False
        while abs(motorRight.get_degrees_counted()) <= abs(deg_start) + 50:
            tank.start_tank(30,30)
            if isGreen('l'):
                isLeftGreen = True
        tank.stop()
        if isLeftGreen:
            u_turn()
        else:
            print('turn right')

def u_turn():
    print('U-turn')

def isGreen(direction):
    if direction == 'l':
        hsv_left = changeRGBtoHSV(colorLeft.get_rgb_intensity())
        return (150 < hsv_left[0] < 180 and hsv_left[1] > 20 and hsv_left[2] > 10)
    else:
        hsv_right = changeRGBtoHSV(colorRight.get_rgb_intensity())
        return (150 < hsv_right[0] < 180 and hsv_right[1] > 20 and hsv_right[2] > 10)

while timer.now() < 10:
    try:
        rgb_left = colorLeft.get_rgb_intensity()
        hsv_left = changeRGBtoHSV(rgb_left)
        if 150 < hsv_left[0] < 180 and hsv_left[1] > 20 and hsv_left[2] > 10:
            print('Left sensor is over green')
            green_intersection('l')
        rgb_right = colorRight.get_rgb_intensity()
        hsv_right = changeRGBtoHSV(rgb_right)
        if 150 < hsv_right[0] < 180 and hsv_right[1] > 20 and hsv_right[2] > 10:
            print('Right sensor is over green')
            green_intersection('r')
        error = (rgb_left[1] - rgb_right[1]) / 4.7
    except:
        print('cannot get RGB')
    u = Kp * error + Ki * (error + last_error) + Kd * (error - last_error)
    tank.start_tank(int(basic_speed + u),int(basic_speed - u))
    count += 1
    wait_for_seconds(0.01)

tank.stop()
print(10/count*1000)
