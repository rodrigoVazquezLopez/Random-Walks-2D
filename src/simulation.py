import datetime
import random
import randomWalks2D as rw
import readTrajectory as rt
import Astar
import threading

def writeFile(filename, data):
    with open(filename, 'w') as file:
        for element in data:
            text = "{}, {},\n".format(element[0], element[1])
            file.write(text)

def producer(queue, evento, dat):
    print("Producer: Iniciando")
    randomTrajectory = rw.generate2DRandomWalk(50)

    for element in randomTrajectory:
        data = [element, 1.0]
        print("Producer: {}".format(data))
        queue.append(data)
    print("Producer: Notificando")
    evento.set()
    
    directoryPath = "./data/Simulation/"
    randomWalkFilename = directoryPath + dat.strftime("randomWalk_%d%b%Y_%H.%M") + ".txt"
    writeFile(randomWalkFilename, randomTrajectory)

    print("Producer: Finalizando")
    

def consumer(queue, evento, dat):
    
    print("Consumer: Iniciando")
    random.seed()
    rNum = random.randint(-200, -120)
    x_i = rNum - (rNum % 10)
    rNum = random.randint(-90, 90)
    y_i = rNum - (rNum % 10)

    rNum = random.randint(170, 200)
    x_f = rNum - (rNum % 10)
    rNum = random.randint(-40, 80)
    y_f = rNum - (rNum % 10)

    p_i = (x_i, y_i)
    p_f = (x_f, y_f)

    inputFilename = "./src/MATLAB/puntos.txt"
    obstacles = rt.readTrajectory(inputFilename)
    print("Consumer: Esperando")
    evento.wait()
    print("Consumer: Continuando")


    while len(queue) > 0:
        data = queue.pop()
        encontrado = False
        for element in obstacles:
            if data[0] in element:
                print("Consumer: {} en obstacles".format(data[0]))
                encontrado = True
                element[1] = 1.0
                break
        if encontrado == False:
            obstacles.append(data)
        
    pathResult = Astar.Aasterisk(p_i, p_f, obstacles)

    directoryPath = "./data/Simulation/"
    obstaclesFilename = directoryPath + dat.strftime("obstacles_%d%b%Y_%H.%M") + ".txt" 
    writeFile(obstaclesFilename, obstacles)

    pathResultFilename = directoryPath + dat.strftime("result_%d%b%Y_%H.%M") + ".txt"
    writeFile(pathResultFilename, pathResult)
    
    print("Consumer: Finalizando")


if __name__ == '__main__':
    print("Main: Iniciando")
    pipeline = []
    dat = datetime.datetime.now()
    evento = threading.Event()

    producerThread = threading.Thread(target=producer, args=(pipeline, evento, dat))
    consumerThread = threading.Thread(target=consumer, args=(pipeline, evento, dat))
    
    producerThread.start()
    consumerThread.start()

    print('Main: Finalizado')

