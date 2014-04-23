# coding=utf-8
from fslib.graph.graph import Graph


class Environment(Graph):
    def __init__(self, dimension, name = "environment"):
        Graph.__init__(self, name)
        self._dim = dimension # the dimension of a space
        self._curr_state = 0


    def get_dimension(self):
        return self._dim

    def distance(self, src, dst):
        #if(src.get_dimension() != dst.get_dimension()):
        dist = 0
        for i in range(0, src.get_dimension()):
            dist += abs(src.coords()[i] - dst.coords()[i])

        return dist**(1.0/2.0)  # Euclidean norm
        #return dst

    def distance_from_current(self, state):  # get distance from current environment state
        return self.distance(self.get_current_state(), state)

    def get_state_by_coords(self, coords):
        if len(coords) != self.get_dimension():
            raise ValueError("invalide number of coordinates")
        return next((p for p in self._vertex_list if (p.coords() == coords)), None)


    def get_current_state(self):
        return self._curr_state

    def set_current_state(self, start):
        if self.is_contains_vertex(start):
            self._curr_state = start
            return True
        return False

    _msg = True
    _count = 0
    def update_state(self, motor_fs):
        tmp_c = motor_fs.change_coords(self.get_current_state().coords())
        curr = self.get_current_state()
        tmp_st = None
        for e in curr.get_outcoming():
            if e.get_dst().coords() == tmp_c:
                tmp_st = e.get_dst()

        if tmp_st is self.get_current_state(): # this case never happens
            self._msg = True
            return

        if tmp_st is None:
            if self._msg:
                print("Нельзя перейти из " + curr.name + " в " + str(tmp_c))
                self._msg = False
            return

        print("Перешли из " + curr.name + " в " + tmp_st.name)
        self.set_current_state(tmp_st)
        self._msg = True


