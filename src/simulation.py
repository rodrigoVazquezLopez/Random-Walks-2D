import random
import randomWalks2D as rw
import readTrajectory as rt
import Astar

import threading
import concurrent.futures
import queue

condition = threading.Condition()

def producer(queue):
    condition.acquire()
    print("Producer: Iniciando")
    randomTrajectory = rw.generate2DRandomWalk()

    for element in randomTrajectory:
        data = [element, 1.0]
        print(data)
        queue.put(data)
    print("Producer: Notificando")
    condition.notify()
    condition.release()

    randomWalkFilename = "../data/Simulation/randomWalk.txt"

    with open(randomWalkFilename, 'w') as file:
        for element in randomTrajectory:
            text = "{}, {}\n".format(element[0], element[1])
            file.write(text)

    condition.release()
    print("Producer: Finalizando")

def consumer(queue):
    
    print("Consumer: Iniciando")
    random.seed()
    rNum = random.randint(-200, -120)
    x_i = rNum - (rNum % 10)
    rNum = random.randint(-200, 200)
    y_i = rNum - (rNum % 10)

    rNum = random.randint(170, 200)
    x_f = rNum - (rNum % 10)
    rNum = random.randint(-40, 90)
    y_f = rNum - (rNum % 10)

    p_i = (x_i, y_i)
    p_f = (x_f, y_f)

    inputFilename = "./src/MATLAB/puntos.txt"
    obstacles = rt.readTrajectory(inputFilename)
    condition.acquire()
    print("Consumer: Esperando")
    condition.wait()
    print("Consumer: Continuando")
    condition.release()

    while not(queue.empty()):
        data = queue.get()
        x = data[0]
        y = data[1]
        for element in obstacles:
            if (x, y) in element:
                element[1] = 1.0
            else:
                point = (x, y)
                data = [point, 1.0]
                obstacles.append(data)

    pathResult = Astar.Aasterisk(p_i, p_f, obstacles)

    obstaclesFilename = "../data/Simulation/obstacles.txt"

    with open(obstaclesFilename, 'w') as file:
        for element in obstacles:
            text = "{}, {}, {}\n".format(element[0], element[1], element[2])
            file.write(text)

    pathResultFilename = "../data/Simulation/result.txt"

    with open(pathResultFilename, 'w') as file:
        for element in pathResult:
            text = "{}, {}\n".format(element[0], element[1])
            file.write(text)

    
    print("Consumer: Finalizando")


if __name__ == '__main__':
    print("Main: Iniciando")
    pipeline = queue.Queue(maxsize=0)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline) # Thread 1 producer
        executor.submit(consumer, pipeline) # Thread 2 consumer

    print('Main: Finalizado')

