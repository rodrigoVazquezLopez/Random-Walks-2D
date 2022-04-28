import random

def generateRandom():
    random.seed()
    r = random.randint(0, 1)
    if r == 0:
        return True
    else:
        return False

def generateRandomWalk2DPoint():
    gap = 10
    x = 0
    y = 0
    if generateRandom():
        x += gap
    else:
        x -= gap
    if generateRandom():
        y += gap
    else:
        y -= gap
    return (x, y)

def generateRandomWalk2DPointV1():
    gap = 10
    x = 0
    y = 0
    random.seed()
    r = random.randint(0, 3)
    if r == 0:
        x += gap
    elif r == 1:
        x -= gap
    elif r == 2:
        y += gap
    else:
        y-= gap
    return (x, y)


def generate2DRandomWalk(n):
    trajectory = []
    x = 0
    y = 0
    trajectory.append((x, y))
    for i in range(n):
        point = generateRandomWalk2DPoint()
        x += point[0]
        y += point[1]
        trajectory.append((x, y))
    
    return trajectory

# if __name__ == '__main__':
#     trajectory = generate2DRandomWalk(50)
#     for element in trajectory:
#         print(element)
#     print("main")