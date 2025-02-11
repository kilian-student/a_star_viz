# standard library
from typing import Optional, Union, Tuple
import random

# Third-party imports
import networkx as nx  # type: ignore
import numpy as np

# Local application imports
from utils.geometry import Point2D
from utils import constants as const

class Node():

    def __init__(self, pos: Point2D, id: int):
        self.pos = pos
        self._id = id
        self.connected_nodes: list[Node] = []
        self._g: float = float('inf')
        self._h: float = float('inf')
        self._f: float = 0
        self._parent: Optional[Node] = None

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, prev_node):
        self._parent = prev_node

    @property
    def h(self) -> float:
        return self._h
    
    @h.setter
    def h(self, cost: float):
        self._h = cost

    @property
    def g(self) -> float:
        return self._g
    
    @g.setter
    def g(self, cost: float):
        self._g = cost

    @property
    def f(self) -> float:
        h = self._h
        g = self._g
        return g + h
    
    @f.setter
    def f(self, cost: float):
        # TODO: prevent direct access here!!
        self._f = cost

    def __hash__(self):
        return hash(self._id)

    
    def __eq__(self, other):
        if isinstance(other, int):
            return self._id == other
        elif not isinstance(other, Node):
            return False
        return self._id == other._id
    
    def __lt__(self, other):
            if not isinstance(other, Node):
                raise NotImplementedError
            return self.f < other.f

    def __le__(self, other):
        if not isinstance(other, Node):
            raise NotImplementedError
        return self.f <= other.f
    
    def __gt__(self, other):
            if not isinstance(other, Node):
                raise NotImplementedError
            return self.f > other.f

    def __ge__(self, other):
        if not isinstance(other, Node):
            raise NotImplementedError
        return self.f >= other.f
    
    def __str__(self):
        return str(self._id)
    
    def __repr__(self):
        return str(self._id)
    


class Graph(nx.Graph):
    """represents the visual and actual graph
    see documenation for nx.Graph: https://networkx.org
    """
    
    def __init__(self, start_node_id: int = 0, target_node_id: int = -1, edge_weight: Union[float, Tuple] = 2):
        super(Graph, self).__init__()
        self._start_node_id = start_node_id
        self._target_node_id = target_node_id
        if not isinstance(edge_weight, tuple):
            if np.abs(int(edge_weight) - edge_weight) < 0.1:
                edge_weight = int(edge_weight)
        self._edge_weight = edge_weight
        
        self.init_nodes()

    def init_nodes(self):
        i = 1
        for y in range(1, 11, 1): # 10 Nodes vertical
            for x in range(1, 21, 1): # 20 Nodes horizontal
                # Knoten erzeugen
                node = Node(Point2D(2*x, 2*y), i)
                self.add_node(node)
                if node._id-1 >= 1 and not (node._id%20==1):
                    node.connected_nodes.append(list(self.nodes)[node._id-2])
                if node._id -20 >= 1:
                    node.connected_nodes.append(list(self.nodes)[node._id-21])
                # Kanten hinzufügen
                for neighbour in node.connected_nodes:
                    edge_weight = self._edge_weight
                    if isinstance(self._edge_weight, tuple):
                        edge_weight = random.randint(self._edge_weight[0], self._edge_weight[1])
                    self.add_edge(node, neighbour, color='blue', weight=edge_weight)
                i+=1

    @property
    def start_node(self) -> Node:
        return list(self.nodes)[self._start_node_id - 1]
    
    @property
    def target_node(self) -> Node:
        return list(self.nodes)[self._target_node_id - 1]



if __name__ == "__main__":
    g = Graph()
    g.plot_graph()