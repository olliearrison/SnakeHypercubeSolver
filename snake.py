

import copy
import random

#* adjacency list representation of n-dimensional hypercube
class Cube:
    def __init__(self, n=1):
        self.d = {0:[1],1:[0]}
        self.max = 1 #* keeps track of max vertex index to simplify logic for labeling
        self.vertexOpen = [True, True]
        for i in range(n-1):
            self.split()

    def newVertex(self):
        self.max += 1
        self.vertexOpen += [True]
        return self.max

    #* changes hypercube from n dimensions to n+1
    def split(self):
        d2 = dict()

        #* make new vertices for all old ones
        oldToNew = dict()

        for key in self.d:
            v = self.newVertex()
            oldToNew[key] = v
            d2[v] = []

        for key in self.d:
            v = oldToNew[key]
            for x in self.d[key]:
                d2[v] += [oldToNew[x]]
                
        self.d.update(d2)
        for key in oldToNew:
            self.d[key] += [oldToNew[key]]
            self.d[oldToNew[key]] += [key]
    
    #TODO: text/potentially fix function
    #* https://stackoverflow.com/questions/64585711/how-can-i-loop-over-the-items-of-a-python-dictionary-in-a-random-order
    def randomize(self):
        for key in self.d:
            random.shuffle(self.d[key])


best = 0
bestL = []
#* build hypercube
cube = Cube(5)
print(cube.d)

def solveSnakeDFS(L, t = 0, verbose=False):
    global best
    global bestL
    if len(L) <= 0:
        return 0

    lastLocation = L[-1]

    for move in cube.d[lastLocation]:
        if cube.vertexOpen[move] and (random.random() > 0):
            #* make move
            origin = dict()
            for connect in cube.d[lastLocation]:
                origin[connect] = cube.vertexOpen[connect]
                cube.vertexOpen[connect] = False
            newMoveSequence = copy.deepcopy(L)
            newMoveSequence.append(move)
            result = solveSnakeDFS(newMoveSequence)
            #TODO: optimize move representation
            if result > best:
                if verbose:
                    print("so far", result-1)
                best = result
                bestL = copy.deepcopy(L)
            for connect in cube.d[lastLocation]:
                cube.vertexOpen[connect] = origin[connect]
    return len(L)


#TODO:
#* given snake that has reached limit, run binsearch ish to determine
#* if sections of the snake can be removed to grow it more in another direction
def rebuildOpenFromPath(path):
    return 42

def verifySolution(dims, path, verbose=True):
    #* fresh cube state
    testCube = Cube(dims)
    testCube.vertexOpen = [True] * (testCube.max + 1)

    if len(path) == 0:
        if verbose:
            print("Empty path.")
        return True

    for i in range(len(path) - 1):
        cur = path[i]
        nxt = path[i + 1]

        #* check adjacency
        if nxt not in testCube.d[cur]:
            if verbose:
                print(f"Invalid move: {cur} -> {nxt} not adjacent.")
            return False

        #* check open
        if not testCube.vertexOpen[nxt]:
            if verbose:
                print(f"Invalid move: {nxt} is closed.")
            return False

        #* apply closing rule
        for connect in testCube.d[cur]:
            testCube.vertexOpen[connect] = False
        testCube.vertexOpen[nxt] = True

    if verbose:
        print("Solution is valid. Length:", len(path))

    return True


print(cube.max)
solveSnakeDFS([0])
result = best - 1
print("Best found length", result)
#* optional:
# cube.randomize()