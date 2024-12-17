# standard lib
from typing import List, Optional

# Third-party imports
import heapq
import networkx as nx  # type: ignore
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

# Local application imports
from utils.geometry import euclidian_distance
from utils.graph import Node, Graph
import utils.constants as const

class A_star():
    """class for executing the algorithm steps
    """

    def __init__(self):
        self.open_list: List[Node] = []
        self.closed_list = set()
        self.current_node : Optional[Node] = None
        self.graph = Graph()
        heapq.heappush(self.open_list, self.graph.start_node)
        self.init_heuristic_estimation()
        self.graph.start_node.g = 0

    def init_heuristic_estimation(self):
        for node in self.graph.nodes:
            distance = const.H_SCALE*euclidian_distance(node.pos, self.graph.target_node.pos)
            node.h = distance

    def go_algo_step(self) -> Node:
            current_node = heapq.heappop(self.open_list)
            self.closed_list.add(current_node)
            if current_node == self.graph.target_node:
                print('Yeah! Target reached!')
                return current_node
            for neighbour in list(self.graph.neighbors(current_node._id)):
                cost_current_to_neighbour = self.graph[current_node._id][neighbour]['weight']
                neighbour_g_new = current_node.g + cost_current_to_neighbour
                #neighbour_f_new = neighbour.h + neighbour_g_new
                if neighbour in self.open_list:
                    if neighbour.g > neighbour_g_new:
                        neighbour.g = neighbour_g_new
                        neighbour.parent = current_node
                elif neighbour in self.closed_list:
                    if neighbour.g > neighbour_g_new:
                        raise NotImplementedError('Closed nodes should not need to be reopened!')
                else:
                    neighbour.g = neighbour_g_new
                    neighbour.parent = current_node
                    heapq.heappush(self.open_list, neighbour)
            return current_node

    def full_run(self) -> bool:
        """Execution of whole Algorithm till end (target reached/open list empty) without stopping.
        Return:
            bool: True if the target node is reached else False
        """
        while self.open_list:
            self.current_node = self.go_algo_step()
            if self.current_node == self.graph.target_node:
                 return True
        return False

    def single_step_run(self) -> bool:
        """Allows execution of single step of the algorith. 
        This mean only one new node from open list is selected and its neighbours updated.
        Raises:
            NotImplementedError: Missing functionality when reached target!!
        Return:
            bool: True if the target node is reached else False
        """
        if not self.open_list:
            raise NotImplementedError('algo finished!!')
        self.current_node = self.go_algo_step()
        if self.current_node == self.graph.target_node:
            return True
        return False

    def plot_graph(self, plt_axes: Optional[Axes] = None, show_current_node = False, show_open = False, show_closed = False, show_ideal_path = False):
        """Plots the current state of the algorithm in matplotlib

        Args:
            plt_axes: matplotlib axes for plotting
            current_node: colors the node in graph which is latest opened
            show_open: colors the nodes in the current open list
            show_closed: colors the nodes in the current closed list
        """
        # retrieve nodes positions
        pos_dict = {}
        for node in self.graph.nodes:
            pos_dict.update({node: (node.pos.x, node.pos.y)})
        # Zeichne den Graphen
        nx.draw(self.graph, pos_dict, ax=plt_axes, with_labels=True, node_color=const.NODE_COLOR_DEFAULT, node_size=const.NODE_SIZE, font_size=16, )
        
        # Use different node colors for node states (Nodes in open list, currently open node)
        if show_open and self.open_list:
            nx.draw_networkx_nodes(self.graph, pos_dict, self.open_list, ax=plt_axes, node_size=const.NODE_SIZE, edgecolors=const.NODE_EDGE_COLOR_OPEN)
        if show_closed and self.closed_list:
            nx.draw_networkx_nodes(self.graph, pos_dict, self.closed_list, ax=plt_axes, node_size=const.NODE_SIZE, node_color=const.NODE_COLOR_CLOSED)
        if show_current_node and self.current_node and show_ideal_path:
            ideal_nodes_list = []
            ideal_node = self.current_node
            while ideal_node.parent:
                ideal_nodes_list.append(ideal_node)
                ideal_node = ideal_node.parent
            nx.draw_networkx_nodes(self.graph, pos_dict, ideal_nodes_list, ax=plt_axes, node_size=const.NODE_SIZE, node_color=const.NODE_COLOR_IDEAL_PATH)
        if show_current_node and self.current_node:
            nx.draw_networkx_nodes(self.graph, pos_dict, [self.current_node], ax=plt_axes, node_size=const.NODE_SIZE, node_color=const.NODE_COLOR_CURRENT)
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, pos_dict, ax=plt_axes, edge_labels=edge_labels, font_color=const.EDGE_COLOR)
        plt.show()


if __name__ == "__main__":
        algo = A_star()
        algo.full_run()