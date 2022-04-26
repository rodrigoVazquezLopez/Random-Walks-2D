import time
import Astar
import random as r

import threading
import concurrent.futures
import queue

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

uriDron1  = 'radio://0/80/2M/E7E7E7E7E7'
uriDron2  = 'radio://0/80/2M/E7E7E7E7E8'

producerIsReady = False
consumerIsReady = False

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

def generateRandom2D(x, y):
    gap = 10
    r = r.randint(0, 1)
    r.seed()
    if r == 0:
        x += gap
    else:
        x -= gap
    r = r.randint(0, 1)
    r.seed()
    if r == 0: 
        y += gap
    else:
        y -= gap
    
    return [x, y]

#--------------- Producer ------------------
def producer(queue):
    x = 0.0
    y = 0.0
    z = 0.4
    trajectory = []

    global producerIsReady
    global consumerIsReady

    for i in range(50):
        res = generateRandom2D(x, y)
        x = res[0]
        y = res[1]
        point = (x, y, z)
        trajectory.append(point)
        queue.put(point)
    
    print("Producer: Trayectoria generada")
    producerIsReady = True

    while consumerIsReady == False:
        time.sleep(0.1)

    with SyncCrazyflie(uriDron1, cf=Crazyflie(rw_cache='./cache1')) as scf1:
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stateEstimate.x', 'float')
        lg_stab.add_variable('stateEstimate.y', 'float')
        lg_stab.add_variable('stateEstimate.z', 'float')
        lg_stab.add_variable('acc.x', 'float')
        lg_stab.add_variable('acc.y', 'float')
        scf1.cf.log.add_config(lg_stab)
        #lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()

        with PositionHlCommander(scf1, default_height=0.4, controller=PositionHlCommander.CONTROLLER_PID) as pc1:
            while len(trajectory) > 0:
                point = trajectory.pop()
                pc1.go_to(point[0]/100, point[1]/100, point[2]/100)
                time.sleep(1)

    print("Producer: Finalizado")



#--------------- Consumer ------------------
def consumer(queue):
    global producerIsReady
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

    inputFilename = "./src/MATLAB/puntos.txt"
    outputFilename = "solution.txt"

    # Leyendo archivo con trayectoria
    trajectoryList = readTrajectory(inputFilename)
    print("Consumer: Trayectoria leida...")

    # for element in trajectoryList:
        # print(element)
    # input("esperando")

    while producerIsReady == False:
        time.sleep(0.1)

    while not(queue.empty()):
        data = queue.get()
        x = data[0]
        y = data[1]
        for element in trajectoryList:
            if (x, y) in element:
                element[1] = 1.0
            else:
                point = (x, y)
                data = [point, 1.0]
                trajectoryList.append(data)

    pathResult = Astar.Aasterisk(p_i, p_f, trajectoryList)

    with SyncCrazyflie(uriDron2, cf=Crazyflie(rw_cache='./cache2')) as scf2:
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stateEstimate.x', 'float')
        lg_stab.add_variable('stateEstimate.y', 'float')
        lg_stab.add_variable('stateEstimate.z', 'float')
        lg_stab.add_variable('acc.x', 'float')
        lg_stab.add_variable('acc.y', 'float')
        scf2.cf.log.add_config(lg_stab)
        #lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()

        with PositionHlCommander(scf2, default_height=0.4, controller=PositionHlCommander.CONTROLLER_PID) as pc2:
            for element in pathResult:
                pc2.go_to(element[0]/100, element[1]/100, 0.4)
                time.sleep(1)

    
    

    with open(outputFilename, 'w') as file:
        for element in pathResult:
            text = "{}, {}\n".format(element[0], element[1])
            file.write(text)


#--------------- Main ------------------
if __name__ == '__main__':

    pipeline = queue.Queue(maxsize=0)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline) # Thread 1 producer
        executor.submit(consumer, pipeline) # Thread 2 consumer

    print('Main: Finalizado')