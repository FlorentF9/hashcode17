import numpy as np
from collections import deque

class node:
    def __init__(self, state, value):
        self.state = state
        self.value = value
        self.neighbours = deque()
        self.mark = False
        self.trace = None


    def linkneighbours(self, list_nodes):
        for node in list_nodes:
            self.neighbours.append(node)
            node.neighbours.append(self)
        return None

    def breadthsearch(self, state):
        queu = deque()
        trash = deque()
        queu.append(self)

        while(len(queu)>0):
            current_node = queu.popleft()
            current_node.mark = True
            if current_node.state == state:
                queu.clear()
            else:
                for n in current_node.neighbours:
                    n.trace = current_node
                    queu.append(n)
            trash.append(current_node)

        path = deque()
        while not current_node==self:
            path.appendleft(current_node)
            current_node = current_node.trace

        path.appendleft(self)

        for k in trash:
            k.mark = False
            k.trace = None

        return path

    def depthsearch(self, state):
        path = deque()
        path.append(self)
        self.mark = True
        if self.state == state:
            return path
        queu = deque()
        queu.extend([noeud for noeud in self.neighbours if not noeud.mark])
        while len(queu)>0:
            current_node = queu.popleft()
            current_node.mark = True
            try_path = current_node.depthsearch(state)
            if try_path is not None:
                path.extend(try_path)
                return path
        return None

    def clean_component(self):
        queu = deque()
        queu.append(self)
        while(len(queu)>0):
            node = queu.popleft()
            node.mark = False
            queu.extend([noeud for noeud in node.neighbours if noeud.mark])
        return None

    def hasting(self, iteractions,To, lda):

        temperature = To
        current_node = self
        for i in range(iteractions):
            queu = deque()
            possibles = [current_node]+list(current_node.neighbours)
            values = np.array([possibles[i].value for i in range(len(possibles))])
            deltas = np.max(values)*np.ones(len(values))- values
            probs = np.exp( - deltas/temperature)
            probs = probs/np.sum(probs)
            ind_node = np.random.choice(len(possibles), p=probs)
            current_node = possibles[ind_node]

            temperature = temperature*lda
            if i%100==0:
                print(temperature, current_node.value)

        return current_node
