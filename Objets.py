from random import random
from math import e, pi
from tkinter import *


###############################################################################################################
# Tkinter
haut, larg = 900, 900

edges = dict()
fenetre = Tk()

###############################################################################################################
# Classes principales

class Vertex():
    
    def __init__(self, idNumb):
        self.id = idNumb
        self.coordX = 0
        self.coordY = 0
        self.adjacence = []
        self.edges = []
        self.chemin = []
        
    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)
        #return "Je suis le sommet {0}, situé aux coordonnées ({1}, {2})".format(str(self.id), str(self.coordX), str(self.coordY))

    def __int__(self):
        return int(self.id)
        
    def getCoord(self, tailleGraph):
        """Mets à jour les coordonnés du vertex en vu de l'affichage"""
        z = (haut/2-50)*e**(pi*2j*self.id/tailleGraph)
        self.coordX = larg/2+z.real
        self.coordY = haut/2+z.imag

    def getDegre(self):
        """Retourne le degré du vertex"""
        return len(self.adjacence)



class Graph():
    
    def __init__(self, probaEdge):
        self.taille = 0
        self.listeSommets = []
        self.probaEdge = probaEdge
        
        self.debug = []
                
    def __str__(self):
        return "Je suis un graphe à " + str(self.taille) + " sommets."
        
    def addVertex(self, n = 1):
        """Ajoute n vertices au graph"""
        for i in range(n):
            self.listeSommets.append(Vertex(i))
        self.taille += n

    def drawGraph(self):
        global edges
        
        for v in self.listeSommets :
            v.getCoord(self.taille)
            canvas.create_oval(v.coordX-5, v.coordY-5, v.coordX+5, v.coordY+5, fill = "blue")
            z = (haut/2-35)*e**(pi*2j*v.id/self.taille)
            x, y = larg/2+z.real, haut/2+z.imag
            canvas.create_text(x, y, text = str(v))

        edges = dict()
        for v in self.listeSommets:
            for idNumb in v.adjacence:
                if idNumb > v.id:
                    edges[str(v.id)+" "+str(idNumb)] = canvas.create_line(v.coordX, v.coordY, self.listeSommets[idNumb].coordX, self.listeSommets[idNumb].coordY, fill = "red")

    def addEdge(self, i, j, sure = False):
        """Ajoute un edge entre les sommets i et j avec la probabilité probaEdge"""
        if random() < self.probaEdge or sure:
            self.listeSommets[i].adjacence.append(j)
            self.listeSommets[i].edges.append(True)
            self.listeSommets[j].adjacence.append(i)
            self.listeSommets[j].edges.append(True)

    def isConnex(self):
        """Retourne si le graphe est connexe ou non"""
        
        if not all([vertex.getDegre() != 0 for vertex in self.listeSommets]):
            return False
        
        checked = set()
        liste = [self.listeSommets[0]]
        while len(liste) != 0 and len(checked) < self.taille:
            vertex = liste.pop(0)
            checked.add(vertex.id)
            for v in vertex.adjacence:
                if v not in checked and self.listeSommets[v] not in liste:
                    liste.append(self.listeSommets[v])
        return self.taille == len(checked)

    def existeTour(self):
        """Retourne s'il existe un tour d'Euler dans le graphe"""
        return self.isConnex() and all([vertex.getDegre()%2 == 0 for vertex in self.listeSommets])


    def findCycle(self, debut = 0):
        """Retourne un cycle dans le graphe a partir du vertex #debut"""
        
        for v in self.listeSommets:
            v.chemin = []
            
        checked = set()
        liste = [self.listeSommets[debut]]
        for n in range(self.taille+5):
            vertex = liste.pop(0)
            checked.add(vertex.id)
            for w in vertex.adjacence:
                if w not in checked and vertex.edges[vertex.adjacence.index(w)] and \
                (len(vertex.chemin) <= 1 or len(self.listeSommets[w].chemin) <= 1 or self.listeSommets[w].chemin[1] != vertex.chemin[1]):
                    v = self.listeSommets[w]
                    if v.chemin != []:
                        return v.chemin + [v.id, vertex.id] + vertex.chemin[::-1]
                    else:
                        v.chemin = vertex.chemin + [vertex.id]
                    liste.append(v)

    def findEulerianTour(self):

        if not self.existeTour():
            return "Il n'y a pas de tour d'Euler possible dans ce graphe"

        else:
            return self.findEulerianTourAux(0)

    def findEulerianTourAux(self, vertex):
        """Retourne un tour d'Euler dans le graphe"""

        # Cas initial :
        # si tous les edges partant de vertex ont déjà été utilisés dans le tour, on retourne rien
        if True not in self.listeSommets[vertex].edges:
            return [vertex]

        # Récurrence :
        # On trouve un cycle
        cycle = self.findCycle(vertex)

        # On met à jour les vertex utilisés dans le cycle :
        for i in range(len(cycle)-1):
            v = self.listeSommets[cycle[i]]
            index =  v.adjacence.index(cycle[i+1])                  # Index d'apparition du vertex \cycle[i+1]\ dans la table d'adjacence
            v.edges[index] = False
            self.debug.append((v.id, index))
            v = self.listeSommets[cycle[i+1]]
            index = v.adjacence.index(cycle[i])
            v.edges[index] = False            

        # Pour chaque sommets de ce cycle, on va trouver un nouveau cycle
        tour = []
        for i in range(0, len(cycle)):
            tour.extend(self.findEulerianTourAux(cycle[i]))

        return tour
        
            



###############################################################################################################
# Main

def createGraph(n = 50, p = 0.25):
    """Retourne un graphe aléatoire de n vertex avec une probabilité d'edge p"""

    graph = Graph(p)
    graph.addVertex(n)
    for i in range(n):
        for j in range(i+1, n):
            graph.addEdge(i, j)
    return graph


def makeEulerian(graph):
    """Ajoute des edges à un graphe jusqu'à ce que celui ci contienne un tour d'Euler"""

    # Gere les vertices de degre n-1
    complet = [vertex for vertex in graph.listeSommets if vertex.getDegre() == graph.taille-1]
    for vertex in complet:
        # Choisis en priorité les voisins de degré impair
        index = sorted(vertex.adjacence, key = lambda v:graph.listeSommets[v].getDegre()%2 == 0)[0]
        indVoisin = vertex.adjacence.index(index)
        vertex.adjacence.pop(indVoisin)
        vertex.edges.pop(indVoisin)
        indVertex = graph.listeSommets[index].adjacence.index(vertex.id)
        graph.listeSommets[index].adjacence.pop(indVertex)
        graph.listeSommets[index].edges.pop(indVertex)

    # Gere les vertices de degre impair
    wrongVertices = [vertex for vertex in graph.listeSommets if vertex.getDegre()%2 == 1 or vertex.getDegre() == 0]
    wrongVertices.sort(key = lambda vertex:len([1 for v in vertex.adjacence if v in wrongVertices]))
    while wrongVertices != []:
        vertex = wrongVertices.pop(0)
        # Filtre les vertices possibles pour faire un lien avec le vertex actuel
        choix = list(filter(lambda v:v.id not in vertex.adjacence, wrongVertices))
        
        # Si on peut faire un lien avec un vertex de degré impair ou de degré nul:
        if choix != []:
            voisin = choix[0]
            graph.addEdge(vertex.id, voisin.id, True)
            if voisin.getDegre() != 1:
                wrongVertices.remove(voisin)
        else:
            # Si aucun vertex ne peut être lié avec le vertex actuel, on en choisit un de degré pair
            # que l'on rajoute dans la liste des vertices de degré impair
            choix = list(filter(lambda v:v.id not in vertex.adjacence and v.id != vertex.id and v.getDegre() < graph.taille-3, graph.listeSommets))
            
            # Si vraiment aucun vertex ne peut être lié, alors on enlève un vertex, en priorité sur les voisins de degré impair
            if choix == []:
                index = sorted(vertex.adjacence, key = lambda v:graph.listeSommets[v].getDegre()%2 == 0)[0]
                indVoisin = vertex.adjacence.index(index)
                vertex.adjacence.pop(indVoisin)
                vertex.edges.pop(indVoisin)
                indVertex = graph.listeSommets[index].adjacence.index(vertex.id)
                graph.listeSommets[index].adjacence.pop(indVertex)
                graph.listeSommets[index].edges.pop(indVertex)
                
                # Si le voisin avait un degré impair, il a maintenant un degré pair:
                # on l'enlève donc de la liste wrongVertices
                if graph.listeSommets[index].getDegre()%2 == 0:
                        wrongVertices.remove(graph.listeSommets[index])

            else:
                voisin = choix[0]
                wrongVertices.append(voisin)
                graph.addEdge(vertex.id, voisin.id, True)
	
        if vertex.getDegre() == 1:
            wrongVertices.append(vertex)


def affiche(graph):
    """Affiche un graphe"""
    canvas.delete("all")
    graph.drawGraph()


g = createGraph(100, 0.125)
print("The graph is connex : ", g.isConnex())
print("The graph has an Eulerian tour : ", g.existeTour())
#for v in g.listeSommets:
#    print str(v) + " : " + ", ".join(map(str, v.adjacence))
if not g.existeTour():
    makeEulerian(g)
print("After modification , the graph has an Eulerian tour : ", g.existeTour())
#for v in g.listeSommets:
#    print(str(v) + " : " + ", ".join(map(str, v.adjacence)))
chemin = g.findEulerianTour()
print(chemin)
print("Taille du chemin : ", len(chemin))
print("Nombre de edges :", sum([v.getDegre() for v in g.listeSommets])//2)



###############################################################################################################
# Fonctions Tkinter

graph = []
indice = 0
tour = []

def maj(graph):
    """Mets à jour le tkinter"""

    canvas.delete("all")
    graph.drawGraph()
    connex.config(text = "Connexité : " + str(graph.isConnex()))
    eulerien.config(text = "Eulerien : " + str(graph.existeTour()))

def generate():
    """Génère un nouveau graphe aléatoire et l'affiche"""
    global graph

    n = int(entryVertices.get())
    p = float(entryProba.get())
    graph = Graph(p)
    graph.addVertex(n)
    for i in range(n):
        for j in range(i+1, n):
            graph.addEdge(i, j)
    maj(graph)
    nextEdgeEuler.grid_remove()
    drawEulerTour.grid(row = 3, column = 5, columnspan = 6)


def makeEuler():
    """Modifie un graphe pour le rendre Eulerien"""
    global graph

    makeEulerian(graph)
    maj(graph)


def drawEuler():
    """Affiche un tour eulerien"""
    global graph, itera, tour

    tour = graph.findEulerianTour()
    drawEulerTour.grid_remove()
    nextEdgeEuler.grid(row = 3, column = 5, columnspan = 2)
    itera = nextEuler(tour)


def nextEuler(tour):
    """Affiche le prochain edge du tour d'Euler"""
    global graph

    for i in range(len(tour)-1):
        if tour[i] < tour[i+1]:
            canvas.itemconfig(edges[str(tour[i])+" "+str(tour[i+1])], fill = "green")
        else:
            canvas.itemconfig(edges[str(tour[i+1])+" "+str(tour[i])], fill = "green")
        yield


def nextEulerEnd():
    global graph, itera

    try:
        next(itera)
    except StopIteration:
        nextEdgeEuler.grid_remove()
        drawEulerTour.grid(row = 3, column = 5, columnspan = 2)


canvas = Canvas(fenetre, width = larg, height = haut, bg = "white")
canvas.grid(row = 2, column = 1, rowspan = 2, columnspan = 4)

connex = Label(fenetre, text = "Connexité")
connex.grid(row = 4, column = 3)

eulerien = Label(fenetre, text = "Eulerien")
eulerien.grid(row = 4, column = 2)

vertices = Label(fenetre, text = "Number of vertices")
vertices.grid(row = 1, column = 1, sticky = E)

proba = Label(fenetre, text = "Probability for edges")
proba.grid(row = 1, column = 3, sticky = E)

entryVertices = Entry(fenetre)
entryVertices.grid(row = 1, column = 2)

entryProba = Entry(fenetre)
entryProba.grid(row = 1, column = 4)

new_graph = Button(fenetre, text = "Generate a new graph", command = generate)
new_graph.grid(row = 2, column = 5)

make_euler = Button(fenetre, text = "Make the graph Eulerian", command = makeEuler)
make_euler.grid(row = 2, column = 6)

drawEulerTour = Button(fenetre, text = "Draw an Eulerian tour", command = drawEuler)
drawEulerTour.grid(row = 3, column = 5, columnspan = 2)

nextEdgeEuler = Button(fenetre, text = "Next", command = nextEulerEnd)
