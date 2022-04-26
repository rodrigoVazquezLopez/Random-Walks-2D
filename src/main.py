import Astar
import random as r

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

uriDron  = 'radio://0/80/2M/E7E7E7E7E7'

def normalizeNumber(num):
    res = num % 10
    if res != 0:
        if res > 5:
            num = num + (10 - res) 
        else:
            num = num - res
    return num


def readTrajectory(filename):
    trajectoryList = []
    with open(filename, 'r') as file:
        for linea in file.readlines():
            tokens = linea.rsplit(',')
            x = float(tokens[0]) * 100
            y = float(tokens[1]) * 100
            p = float(tokens[2])
            x = normalizeNumber(x)
            y = normalizeNumber(y)

            if p >= 0.5:
                points = [(x, y), (x, y + 10), (x, y - 10), (x + 10, y), (x - 10, y)]
                for point in points:
                    isOnlist = False
                    for data in trajectoryList:
                        if point in data:
                            isOnlist = True
                            break
                    if isOnlist == False:
                        element = [point, p]
                        trajectoryList.append(element)
            if p >= 0.25 and p < 0.5:
                element = [(x, y), p]
                trajectoryList.append(element)
            
    return trajectoryList

if __name__ == '__main__':
    r.seed()
    rNum = r.randint(-200, -120)
    x_i = rNum - (rNum % 10)
    rNum = r.randint(-200, 200)
    y_i = rNum - (rNum % 10)

    rNum = r.randint(170, 200)
    x_f = rNum - (rNum % 10)
    rNum = r.randint(-40, 90)
    y_f = rNum - (rNum % 10)

    p_i = (x_i, y_i)
    p_f = (x_f, y_f)

    #s = (-1.7, 0.2)
    #f = (1.4, 1.4)

    #p_i = (s[0] * 100, s[1] * 100)
    #p_f = (f[0] * 100, f[1] * 100)

    inputFilename = "./src/MATLAB/puntos.txt"
    outputFilename = "solution.txt"
    
    # Leyendo archivo con trayectoria
    trajectoryList = readTrajectory(inputFilename)
    print("Trayectoria leida...")
    

    for element in trajectoryList:
        print(element)
    input("esperando")

    pathResult = Astar.Aasterisk(p_i, p_f, trajectoryList)

    with open(outputFilename, 'w') as file:
        for element in pathResult:
            text = "{}, {}\n".format(element[0], element[1])
            file.write(text)