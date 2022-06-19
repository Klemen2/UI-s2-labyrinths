from tkinter import *
from collections import defaultdict
import os
import colorsys
from astar import Astar
from dfs import Dfs
from bfs import Bfs

def def_value():
    return "white"

class Window:
    algorithms = ["A*","BFS","DFS"]#,"IDDFS","IDA*" ]
    classes = [Astar,Bfs,Dfs]
    minCellSize = 50
    maxWindowSize = 700
    steps = None
    currectStep=0
    cost = None
    status = None

    def createHexList(self,hue):
        temp = []
        for i in range(90, 10, -5):
            temp.append("#")
            for j in colorsys.hls_to_rgb(hue,i/100,1):
                temp[-1]+=hex(round(j*255)).split("x")[1]
        return temp
    color = defaultdict(def_value)
    color[-1] = "black"
    color[-2] = "red"
    color[-3] = "yellow"
    color[-4] = "green"

    def __init__(self, title="Seminarska 2", file="", path=None ):
        self.root = Tk()
        self.root.title(title+" "+file)
        self.root.resizable(False, False)
        self.root.configure(bg='#f1f1f1')
        if(path):
            self.color["active"] = self.createHexList(0.77)
            self.color["path"] = self.createHexList(0.66)
            self.algorithm(title,file,path)
        else:
            self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"labyrinths")
            Label(self.root, text="Path to labyrinths: ").grid(row=0, column=0, padx=10)
            self.input = Text(self.root,height=3, width=45)
            self.input.insert(INSERT,self.path)
            self.input.grid(row=0, column=1, padx=10, pady=8)
            Button(self.root, height=2, width=10, text="Refresh", command = lambda:self.refreshMenu()).grid(row=0, column=2, padx=10)
            Label(self.root, text="Labyrinths: ").grid(row=1, column=0)
            self.menu = None
            self.refreshMenu()
            Label(self.root, text="Algorithms: ").grid(row=2, column=0)
            self.selectedAlgorithm = StringVar(self.root)
            self.algorithms = [ "{:<80}".format(i) for i in self.algorithms ]
            self.selectedAlgorithm.set(self.algorithms[0])
            self.algorithmsMenu = OptionMenu(self.root, self.selectedAlgorithm, *self.algorithms)
            self.algorithmsMenu.grid(row=2, column=1, pady=8)
            self.algorithmsMenu.config(width=45)
            Button(self.root, height=2, width=10, text="Start", command = lambda:self.startAlgorithm()).grid(row=1,rowspan=2, column=2, padx=10)

        self.root.mainloop()

    def refreshMenu(self):
        self.path = self.input.get("1.0",END).strip()
        self.files = ["{:<80}".format(f)  for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f)) and "labyrinth" in f ]
        self.selectedFile = StringVar(self.root)
        if (self.menu):
            self.menu.destroy()
        if (len(self.files) > 0):
            self.selectedFile.set(self.files[0])
            self.menu = OptionMenu(self.root, self.selectedFile, *self.files)
        else:
            self.menu = Label(self.root, text="No files")
        self.menu.grid(row=1, column=1)
        self.menu.config(width=45)

    def startAlgorithm(self):
        if(self.selectedFile.get()):
            Window(self.selectedAlgorithm.get().strip(), self.selectedFile.get().strip(),self.path)

    def algorithm(self,algorithm,file,path):
        self.frame = Frame(self.root);
        self.frame.pack()
        self.stepInput = Label(self.frame, text="Calculating")
        self.stepInput.pack(side=LEFT)
        self.frame2 = Frame(self.root)
        self.frame2.pack(fill="both", expand=True)
        self.canvas = Canvas(self.frame2)
        self.canvas.pack(fill="both", expand=True)
        self.frame3 = Frame(self.root)
        self.frame3.pack()
        self.cost = Label(self.frame3, text="Cena: ?")
        self.cost.pack(side=LEFT)
        self.maze = []
        with open(os.path.join(path,file),"r") as f:
            for i in f.readlines():
                self.maze.append(list(int(j) for j in i.strip().split(",")))
        self.drawMaze()
        print(algorithm)
        for i,j in enumerate(self.algorithms):
            if(j==algorithm):

                self.classes[i](self)
                break

    def drawMaze(self):
        cellSize = min(self.minCellSize,int(self.maxWindowSize/len(self.maze)));
        half = cellSize/2
        self.root.geometry(str(len(self.maze)*cellSize)+"x"+str(len(self.maze[0])*cellSize+50))
        self.cells = []
        self.status = []
        for i, value in enumerate(self.maze):
            self.cells.append([])
            self.status.append([])
            for j, cell in enumerate(value):
                self.cells[-1].append(self.canvas.create_rectangle(i*cellSize, j*cellSize, (i+1)*cellSize, (j+1)*cellSize, fill=self.color[cell], outline=self.color[cell]))
                self.status[-1].append([])
                self.canvas.create_text(i*cellSize+half,j*cellSize+half,text=cell)

    def setSteps(self,steps,cost,depth,compare):
        self.cost.config(text = f"Moves: {len(steps)}, Cost: {cost}, Depth: {depth}, Compare: {compare}")
        self.steps = steps
        self.stepInput.destroy()
        self.stepInput = Entry(self.frame, validate="key")
        self.stepInput["validatecommand"]=(self.stepInput.register(self.changedInput),'%P','%S','%d')
        self.stepInput.insert(0, 0)
        Button(self.frame, height=1, width=10, text="Start", command=lambda: self.changeStep(0)).pack(side=LEFT)
        Button(self.frame, height=1, width=10, text="Previous", command=lambda: self.previous()).pack(side=LEFT,padx=10)
        self.stepInput.pack(side=LEFT)
        Button(self.frame, height=1, width=10, text="Next", command=lambda: self.next()).pack(side=LEFT,padx=10)
        Button(self.frame, height=1, width=10, text="Finish", command=lambda: self.changeStep(len(self.steps))).pack(side=LEFT)

    def changedInput(self,value,insert,change):
        if(change=="1"):
            if(insert not in ["1","2","3","4","5","6","7","8","9","0"]):
                return False
            if(value):
                self.changeStep(int(value))
                return True
            return False
        return True

    def changeStep(self,selected):
        if (selected >= len(self.steps)):
            selected = len(self.steps)
        elif (selected <= 0):
            selected = 0
        self.stepInput.delete(0, END)
        self.stepInput.insert(0, selected)
        while (selected > self.currectStep):
            self.changeCell(self.steps[self.currectStep], 1)
            self.currectStep += 1
        while (selected < self.currectStep):
            self.currectStep -= 1
            self.changeCell(self.steps[self.currectStep], -1)

    def previous(self):
        if(self.steps and self.currectStep>0):
            self.currectStep -= 1
            self.changeCell(self.steps[self.currectStep], -1)
            self.stepInput.delete(0, END)
            self.stepInput.insert(0, self.currectStep)

    def next(self):
        if (self.steps and self.currectStep<len(self.steps)):
            self.changeCell(self.steps[self.currectStep],1)
            self.currectStep += 1
            self.stepInput.delete(0, END)
            self.stepInput.insert(0, self.currectStep)


    def changeCell(self,cell,add):
        if(add==1):
            self.status[cell[0]][cell[1]].append(cell[2])
        else:
            self.status[cell[0]][cell[1]].pop()
        if (self.status[cell[0]][cell[1]]):
            if (len(cell) == 4):
                color = self.color["path"][self.status[cell[0]][cell[1]][-1]]
            else:
                color = self.color["active"][self.status[cell[0]][cell[1]][-1]]
        else:
            color = self.color[self.maze[cell[0]][cell[1]]]
        self.canvas.itemconfig(self.cells[cell[0]][cell[1]], fill= color, outline=color)

if __name__ == '__main__':
    window = Window()
