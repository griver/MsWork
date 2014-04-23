
from fslib import Graph
from fslib import BaseMotor
from fslib import BaseSecondary
from fslib import BaseMotivational
from fslib import MotorFS


class CompetitiveNetwork(object):
    def __init__(self, edge_weight):
        self.eweight = edge_weight
        self.vertices = []

    def add_fs(self, fs):
        self.vertices.append(fs)





class BaseFSNetwork(Graph):
    MOTOR_NET = "MOTOR"
    MOTIV_NET = "MOTIV"
    def __init__(self, motor_edges_weight, sec_edges_weight, motiv_edges_weight,  name="FSNetwork"):
        Graph.__init__(self, name)
        self._act_weight = motor_edges_weight
        self._motiv_weight = motiv_edges_weight
        self._sec_weight = sec_edges_weight

        self._cnets = {}
        self.create_cnet(self.MOTOR_NET, motor_edges_weight)
        self.create_cnet(self.MOTIV_NET, motiv_edges_weight)

    def reset_all(self):
        for fs in self._vertex_list:
            fs.reset()

    def recalc_all(self):
        for fs in self._vertex_list:
            fs.recalculate_params()

    def apply_all(self):
        for fs in self._vertex_list:
            fs.apply_new_params()

    def add_motor(self, fs):
        self.add_in_cnet(fs, self.MOTOR_NET)

    def add_motiv(self, fs):
        self.add_in_cnet(fs, self.MOTIV_NET)

    def all_motor(self):
        return self.filter_by_type(BaseMotor)

    def all_secondary(self):
        return self.filter_by_type(BaseSecondary)

    def all_motiv(self):
        return self.filter_by_type(BaseMotivational)

    def get_actions(self):
        result = []
        for fs in filter(lambda fs: isinstance(fs, MotorFS), self._vertex_list):
            if fs.is_active():
                result.append(fs)
        return result

    def filter_by_type(self, type):
        return filter(lambda v: isinstance(v, type), self.vertices())

    def find_fs(self, predicate):
        return filter(predicate, self.vertices())

    def create_cnet(self, name, edge_weight):
        if name in self._cnets:
            raise ValueError("Competitive network with this name already exist")
        self._cnets[name] = CompetitiveNetwork(edge_weight)

    def get_cnet(self, name):
        return self._cnets[name]

    def add_in_cnet(self, fs, cnet_name):
        assert fs.get_cnet_name() is None
        id = self.add_vertex(fs)
        cnet = self.get_cnet(cnet_name)

        if fs in cnet.vertices:
            raise ValueError("Competitive network already include this functional system")

        for v in cnet.vertices:
            self.add_edge(fs, v, cnet.eweight)
            self.add_edge(v, fs, cnet.eweight)

        cnet.add_fs(fs)
        fs.set_cnet_name(cnet_name)
        return id