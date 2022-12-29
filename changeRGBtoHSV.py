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
