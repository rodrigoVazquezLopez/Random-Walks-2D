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