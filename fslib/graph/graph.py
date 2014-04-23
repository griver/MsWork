from fslib.graph.edge import *
class Graph(object) :

    def __init__(self, name) :
        self._vertex_list = []
        self._edge_list = []
        self._name = name


    def add_vertex(self, vertex):
        if self.is_contains_vertex(vertex) :
            return -1
        vertex._set_id(len(self._vertex_list))
        self._vertex_list.append(vertex)
        return vertex.get_id()

    def get_vertices_number(self):
        return len(self._vertex_list)

    def remove_vertex(self, vertex):
        if self.is_contains_vertex(vertex):
            self._vertex_list.pop(vertex)
            return True
        return False

    def remove_vertex_by_id(self, index):
        if self.__check_vertex_id(index):
            self._vertex_list.pop(index)
            return True
        return False

    def is_contains_vertex(self, item):
        if not self.__check_vertex_id(item.get_id()): return False
        return self._vertex_list[item.get_id()] == item

    def get_vertex(self, id):
        return self._vertex_list[id]

    def vertices(self):
        return tuple(self._vertex_list)

    def add_edge(self, src, dst, weight):
        if self.is_contains_vertex(src) and self.is_contains_vertex(dst):
            return Edge(src, dst, weight)

    def remove_edge(self, edge):
        if self.is_contains_vertex(edge.get_src()) and self.is_contains_vertex(edge.get_dst()):
            edge.remove()
            return True
        return False

    def __check_vertex_id(self, id):
        if 0 <= id < self.get_vertices_number():
            return True
        return False

    def __str__(self):
        result = "digraph " + self._name + " {\n"
        for v in self._vertex_list:
            result += "   v"+ str(v.get_id()) + " [label=\""+v.name+"\"];\n"

        for v in self._vertex_list:
            for e  in v.get_outcoming():
                result += "   v" + str(v.get_id()) + " -> v" + str(e.get_dst().get_id())
                result += " [label=\""+ str(e.weight()) + "\"];\n"

        result += "}"
        return result

    def write_to_file(self, filename = None):
        if filename is None: filename = self._name + ".dot"
        f = open(filename, 'w')
        f.write(self.__str__())
        f.close()

