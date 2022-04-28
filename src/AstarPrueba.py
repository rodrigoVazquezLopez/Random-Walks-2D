import datetime
import random
import time
import Astar
from os import fdopen
import logging
import readTrajectory as rt

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

uriDron1  = 'radio://0/80/2M/E7E7E7E7E7'

dronPositions = []

logging.basicConfig(level=logging.ERROR)

def log_stab_callback(timestamp, data, logconf):
    global dronPositions
    # print('[%d][%s]: %s' % (timestamp, logconf.name, data))
    position = (timestamp, data["stateEstimate.x"], data["stateEstimate.y"], data["stateEstimate.z"], data["acc.x"], data["acc.y"])
    dronPositions.append(position)

if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

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

    pathResult = Astar.Aasterisk(p_i, p_f, obstacles)

    dat = datetime.datetime.now()
    directoryPath = "./data/Astar/"
    pathResultFilename = directoryPath + dat.strftime("Solution_%d%b%Y_%H.%M_log") + ".txt"

    with open(pathResultFilename, 'w') as file:
        for element in pathResult:
            text = "{}, {}\n".format(element[0], element[1])
            file.write(text)

    with SyncCrazyflie(uriDron1, cf=Crazyflie(rw_cache='./cache1')) as scf1:
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stateEstimate.x', 'float')
        lg_stab.add_variable('stateEstimate.y', 'float')
        lg_stab.add_variable('stateEstimate.z', 'float')
        lg_stab.add_variable('acc.x', 'float')
        lg_stab.add_variable('acc.y', 'float')
        scf1.cf.log.add_config(lg_stab)
        lg_stab.data_received_cb.add_callback(log_stab_callback)
        lg_stab.start()

        with PositionHlCommander(scf1, default_height=0.4, controller=PositionHlCommander.CONTROLLER_PID) as pc1:
            z = 0.4
            for point in pathResult:
                pc1.go_to(point[0]/100, point[1]/100, z)
                time.sleep(0.1)

        lg_stab.stop()

    dronpostionsFilename = directoryPath + dat.strftime("Vuelo_%d%b%Y_%H.%M_log") + ".txt"
    
    with open(dronpostionsFilename, 'w') as f:
        for elem in dronPositions:
            text = "{}, {}, {}, {}, {}, {}\n".format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5])
            f.write(text)
