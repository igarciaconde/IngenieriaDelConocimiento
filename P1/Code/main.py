from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import math
import heapq
import numpy as np
import time



class Node():

    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position

        self.h = 0
        self.g = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class State():
    
    def __init__(self):
        self.start = [-1,-1]
        self.end = [-1,-1]
        self.able = False

        self.putIni = False
        self.putEnd = False
        self.putObs = False
        self.putWall = False
        self.putCle = False
        self.buttonFlagList = list()
        self.buttonFlagList.append(self.putIni)
        self.buttonFlagList.append(self.putEnd)
        self.buttonFlagList.append(self.putIni)
        self.buttonFlagList.append(self.putIni)
        self.buttonFlagList.append(self.putCle)

        self.lastIniR = None
        self.lastIniC = None
        self.lastEndR = None
        self.lastEndC = None

        self.board = []
        self.buttonList = list()
        self.buttonControlList = list()
        for x in range(24):
            self.board.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
            self.buttonList.append(list())


    def retracePath(self, current_node, maze, able):
        #Esta lista contendrá el camino del fin al inicio
        path = []
        #Obtenemos el numero de rows y de columnas
        current_node
        while current_node is not None:
            path.append(current_node.position)
            current_node = current_node.parent
        #Le damos la vuelta a la lista0,0,0,0,0,0,0,0,0,0,0,0
        path.pop()
        path = path[::-1]
        path.pop()
        self.able = able
        return path

    def aStar(self, graph, start, end):
        
        #inicializamos el nodo slida, el nodo meta, la lista cerrada y la lista abierta
        start_node = Node(None,tuple(start))
        end_node = Node(None,tuple(end))
        yet_to_visit = []
        visited = []
        
        #incluimos el nodo de salida en la lista cerrada
        yet_to_visit.append(start_node)
        #añadimos una condición de stop
        iterations = 0
        

        #definimos los movimientos
        moves = [[-1,0],#arriba
                    [0,-1],#izquierda 
                    [1,0],#abajo
                    [0,1],#derecha 
                    [-1,-1],#diagonalArrIzq
                    [-1,1],#diagonalArrDer
                    [1,-1],#diagonalDebIzq
                    [1,1]] #diagonalDebDer

        n_rows, n_cols = np.shape(graph)
        max_iterations = n_rows * n_cols

        while len(yet_to_visit) > 0:
            #sumamos una iteracion al algoritmo
            iterations += 1

            #sacamos el primer nodo de la lista de abiertos, y comprobamos si alguno de la lista es menor que el,
            #si es así lo sacamos y lo intercambiamos por el otro
            current_node = yet_to_visit[0]
            current_index = 0
            for index, node in enumerate(yet_to_visit):
                if(node.f < current_node.f):
                    current_node = node
                    current_index = index

            #salimos si el problema no tiene solución
            if(iterations >= max_iterations):
                print("No solution for the problem")
                return self.retracePath(current_node, graph, False)
            #añadimos el nuevo current y sacamos el viejo
            yet_to_visit.pop(current_index)
            visited.append(current_node)
        
            #si es solucion devolvemos el path
            if current_node == end_node:
                return self.retracePath(current_node, graph, True)

            #generamos la lista de nodos adyacentes al actual

            child_nodes = []

            for new_position in moves:

                node_position = (current_node.position[0] + new_position[0],
                                current_node.position[1] + new_position[1])
                
                #vemos si nos salimos del tablero
                if (node_position[0] > (n_rows - 1) or node_position[0] < 0 or node_position[1] > (n_cols -1) or node_position[1] < 0):
                    continue

                #comprobamos el nodo
                if graph[node_position[0]][node_position[1]] == 1:
                    continue

                # Creamos un nuevo nodo
                new_node = Node(current_node, node_position)
                # añadimos a la lista de hijos
                child_nodes.append(new_node)

            # recorremos los hijos
            for child in child_nodes:
                
                # Buscamos si están en la visited list
                if len([visited_child for visited_child in visited if visited_child == child]) > 0:
                    continue
                
                #calculamos la distancia al padre en función de la pos del hijo
                if (child.position[0] != current_node.position[0] and child.position[1] != current_node.position[1]):
                    child.g = math.sqrt(2)
                else:
                    child.g = 1
                    
                ## distancia heuristica a la meta 
                child.h = math.sqrt (((end_node.position[0] - child.position[0]) ** 2) + ((end_node.position[1] - child.position[1]) ** 2))
                
                #peso del nodo hijo
                child.f = child.g + child.h
                #penalización si es una zona lenta
                if (graph[child.position[0]][child.position[1]] == 2):
                    child.f += 0.1 * child.f
                # ya esta en la lista de abiertos con un valor menor
                if len([i for i in yet_to_visit if child == i and child.g > i.g]) > 0:
                    continue

                # añadimos los nodos hijo a los abiertos
                yet_to_visit.append(child)

            
    def clearButtonC(self):
        for x in range(5):
            self.buttonControlList[x]['highlightbackground'] = 'lightgrey'
            self.buttonControlList[x]['bg'] = 'lightgrey'

    def printBoard(self):
        for x in range(24):
            for y in range(24):
                if self.board[x][y] == 0:
                    self.buttonList[x][y]['highlightbackground'] = 'black'
                    self.buttonList[x][y]['bg'] = 'black'
                elif self.board[x][y] == 1:  
                    self.buttonList[x][y]['highlightbackground'] = 'blue'
                    self.buttonList[x][y]['bg'] = 'blue'
                elif self.board[x][y] == 2:
                    self.buttonList[x][y]['highlightbackground'] = 'yellow'
                    self.buttonList[x][y]['bg'] = 'yellow'
                elif self.board[x][y] == 3:
                    self.buttonList[x][y]['highlightbackground'] = 'green'
                    self.buttonList[x][y]['bg'] = 'green'
                elif self.board[x][y] == 4:
                    self.buttonList[x][y]['highlightbackground'] = 'red'
                    self.buttonList[x][y]['bg'] = 'red'
                elif self.board[x][y] == 10:
                    self.buttonList[x][y]['highlightbackground'] = 'orange'
                    self.buttonList[x][y]['bg'] = 'orange'
    
    def printResult(self, path):
        for i in range(len(path)):
            if(path[i] != self.start and path[i] != self.end):
                self.board[path[i][0]][path[i][1]] = 10
                self.printBoard()
        if self.able == False:
            messagebox.showinfo("Impossible","No solution for the problem")
            
    
    def onClickControl(self, pos):
        for x in range(5):
            if x == pos:
                self.buttonFlagList[x] = True
            else:
                self.buttonFlagList[x] = False
                self.buttonControlList[x]['highlightbackground'] = 'lightgrey'
                self.buttonControlList[x]['bg'] = 'lightgrey'
        if pos == 0:
            self.buttonControlList[pos]['highlightbackground'] = 'green'
            self.buttonControlList[pos]['bg'] = 'green'
        elif pos == 1:
            self.buttonControlList[pos]['highlightbackground'] = 'red'
            self.buttonControlList[pos]['bg'] = 'red'
        elif pos == 2:
            self.buttonControlList[pos]['highlightbackground'] = 'blue'
            self.buttonControlList[pos]['bg'] = 'blue'
        elif pos == 3:
            self.buttonControlList[pos]['highlightbackground'] = 'yellow'
            self.buttonControlList[pos]['bg'] = 'yellow'
        elif pos == 4:
            self.buttonControlList[pos]['highlightbackground'] = 'grey'
            self.buttonControlList[pos]['bg'] = 'grey'
            

    def onCellClick(self, row, column):
        for pos in range(5):
            if self.buttonFlagList[pos] == True:
                if pos == 0:
                    if self.lastIniR is not None:
                        self.board[self.lastIniR][self.lastIniC] = 0
                    self.board[row][column] = 3
                    self.start = [row,column]
                    self.lastIniR = row
                    self.lastIniC = column
                elif pos == 1:
                    if self.lastEndR is not None:
                        self.board[self.lastEndR][self.lastEndC] = 0
                    self.board[row][column] = 4
                    self.end = [row, column]
                    self.lastEndR = row
                    self.lastEndC = column
                elif pos == 2:
                    if row == self.start[0] and column == self.start[1]:
                        self.start = [-1,-1]
                    if row == self.end[0] and column == self.end[1]:
                        self.end = [-1,-1]
                    self.board[row][column] = 1
                elif pos == 3:
                    if row == self.start[0] and column == self.start[1]:
                        self.start = [-1,-1]
                    if row == self.end[0] and column == self.end[1]:
                        self.end = [-1,-1]
                    self.board[row][column] = 2
                elif pos == 4:
                    if row == self.start[0] and column == self.start[1]:
                        self.start = [-1,-1]
                    if row == self.end[0] and column == self.end[1]:
                        self.end = [-1,-1]
                    self.board[row][column] = 0
        self.printBoard()

    def addToButtonList(self, x, button):
        self.buttonList[x].append(button)
    
    def addToControlList(self, button):
        self.buttonControlList.append(button)

    def restart(self):
        self.start = [-1,-1]
        self.end = [-1,-1]

        for i in range(5):
            self.buttonFlagList[i] = False

        self.lastIniR = None
        self.lastIniC = None
        self.lastEndR = None
        self.lastEndC = None

        for x in range(24):
            for y in range(24):
                self.board[x][y] = 0
        self.printBoard()
        self.clearButtonC()
        for i in range(6):
                self.buttonControlList[i]['state'] = 'normal'
    
    def startmethod(self):
        if self.start == [-1,-1] or self.end == [-1,-1]:
            messagebox.showerror("Cancelled", "You must define init and end point")
            return
        else:
            for i in range(6):
                self.buttonControlList[i]['state'] = 'disabled'
            self.clearButtonC()
            result = self.aStar(self.board, self.start, self.end)
            self.printResult(result)


def main():
    #########
    state = State()
    root = Tk()
    root.resizable(False,False)
    root.geometry('900x646')
    root.title("AStar")

    tab = Canvas(root, width=600, height=646)
    controlSet = Canvas(root, width=300, height= 646, borderwidth=1, relief="raised")
    tab.pack(side='left')
    controlSet.pack(side='left')

    for x in range(24):
        for y in range(24):
            button = Button(master=tab, command=lambda row=x, column=y: state.onCellClick(row, column), highlightbackground='black', bg='black' ,pady=2, relief=FLAT)
            button.grid(row=y,column=x)
            state.addToButtonList(x,button)

    ini = Button(master=controlSet, text='Put start', command=lambda pos=0: state.onClickControl(pos), width=20)
    state.addToControlList(ini)
    ini.pack(side = TOP, expand=YES)
    end = Button(master=controlSet, text='Put end', command=lambda pos=1: state.onClickControl(pos), width=20)
    state.addToControlList(end)
    end.pack(side = TOP, expand=YES)
    wall = Button(master=controlSet, text='Put wall', command=lambda pos=2: state.onClickControl(pos), width=20)
    state.addToControlList(wall)
    wall.pack(side = TOP, expand=YES)
    obs = Button(master=controlSet, text='Put obstacle', command=lambda pos=3: state.onClickControl(pos), width=20)
    state.addToControlList(obs)
    obs.pack(side = TOP, expand=YES)
    cle = Button(master=controlSet, text='Clear Cell', command=lambda pos=4: state.onClickControl(pos), width=20)
    state.addToControlList(cle)
    cle.pack(side=TOP, expand=YES)


    start = Button(master=controlSet, text='RUN', command=lambda: state.startmethod(), width=20, highlightbackground='black')
    state.addToControlList(start)
    start.pack(side = TOP, expand=YES)
    restart = Button(master=controlSet, text='RESTART', command=lambda: state.restart(), width=20, highlightbackground='black')
    state.addToControlList(restart)
    restart.pack(side = TOP, expand=YES)

    controlSet.pack(fill=BOTH, expand=YES)
    root.mainloop()

if __name__ == '__main__':
    main()


