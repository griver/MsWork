from fslib import Environment
import numpy as np
import numpy.random as rnd
from stochastic_transit import StochasticTransit


class StochasticTransitsGroup(object):
    def __init__(self):
        self.edges = []
        self.mins = []
        self.maxs = []
        self.value = None

    def next_value(self):
        self.value = rnd.random()

    def add_edge(self, edge, min_val, max_val):
        self.edges.append(edge)
        self.mins.append(min_val)
        self.maxs.append(max_val)
        edge.set_stochastic_group(self)

    def remove_edge(self, edge):
        i = self.edges.index(edge)
        self.edges.remove(edge)
        self.mins.remove(self.mins[i])
        self.maxs.remove(self.maxs[i])

    def recalc(self):
        self.next_value()
        for i in xrange(0, len(self.edges)):
            self.edges[i].set_availability(self.mins[i] <= self.value < self.maxs[i])

    def clear(self):
        for e in self.edges:
            e.set_availability(True)
            e.set_stochastic_group(None)


def random_array(values, probabilities, size=1):
    if not isinstance(values, np.ndarray):
        values = np.array(values)
    bins = np.add.accumulate(probabilities)
    return values[np.digitize(rnd.random_sample(size), bins)]


class StochasticEnvironment(Environment):


    def __init__(self, dimension, name="Environment", start_state_id=0):
        Environment.__init__(self, dimension, name, start_state_id)
        self._stoch_groups = []

    def create_competitive_group(self, edges, probs=tuple()):
        prob_sum = reduce(lambda x, y: x+y, probs, 0)
        edges_len = len(edges)
        prob_len = len(probs)

        if prob_len == edges_len:
            if prob_sum > 1.0:
                raise ValueError("sum of the probabilities must be <= 1.0")
        elif prob_len < edges_len:
            if prob_sum >= 1.0:
                raise ValueError("sum of the probabilities must be less than 1.0")

        if reduce(lambda x, y: x * (y.get_stochastic_group() is None), edges, True) is False:
            print("at least one of edges already has a group!")

        group = StochasticTransitsGroup()
        curr = 0.0
        for i in xrange(0, edges_len):
            if prob_len > i:
                max_val = curr + probs[i]
            else:
                max_val = curr + (1.0 - curr)/(edges_len - i)
            group.add_edge(edges[i], curr, max_val)
            curr = max_val
        self._stoch_groups.append(group)
        group.recalc()

    def create_united_group(self, edges, probability):
        probability = min(1.0, probability)

        if reduce(lambda x, y: x * (y.get_stochastic_group() is None), edges, True) is False:
            print("at least one of edges already has a group!")

        group = StochasticTransitsGroup()

        for i in xrange(len(edges)):
            group.add_edge(edges[i], 0.0, probability)

        self._stoch_groups.append(group)
        group.recalc()



    def add_edge(self, src, dst, weight=1):
        if self.is_contains_vertex(src) and self.is_contains_vertex(dst):
            return StochasticTransit(src, dst, weight)

    def reset(self):
        Environment.reset(self)
        for g in self._stoch_groups:
            g.recalc()

    def remove_stochasticity(self):
        for g in self._stoch_groups:
            g.clear()
        self._stoch_groups = []
