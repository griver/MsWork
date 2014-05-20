from fslib import Environment
import numpy.random as rnd
from stochastic_transit import StochasticTransit

class StochasticTransitsGroup(object):
    edges = []
    mins = []
    maxs = []
    value = None

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
        for i in range(0, len(self.edges)):
            self.edges[i].set_availability(self.mins[i] <= self.value < self.maxs[i])

    def clear(self):
        for e in self.edges:
            e.set_availability(True)
            e.set_stochastic_group(None)

class StochasticEnvironment(Environment):
    _stoch_groups = []

    def set_probability_to_edges(self, edges, probs=tuple()):
        prob_sum = reduce(lambda x, y: x+y, probs, 0)
        edges_len = len(edges)
        prob_len = len(probs)

        if prob_len == edges_len:
            if prob_sum != 1.0:
                raise ValueError("sum of the probabilities must be 1.0")
        elif prob_len < edges_len:
            if prob_sum >= 1.0:
                raise ValueError("sum of the probabilities must be less than 1.0")

        if reduce(lambda x, y: x * (y.get_stochastic_group() is None), edges, True) is False:
            print("at least one of edges already has a group!")

        group = StochasticTransitsGroup()
        curr = 0.0
        for i in range(0, edges_len):
            if prob_len > i:
                max_val = curr + probs[i]
            else:
                max_val = curr + (1.0 - curr)/(edges_len - i)
            group.add_edge(edges[i], curr, max_val)
            curr += max_val
        self._stoch_groups.append(group)
        group.recalc()

    def add_edge(self, src, dst, weight=1):
        if self.is_contains_vertex(src) and self.is_contains_vertex(dst):
            return StochasticTransit(src, dst, weight)

    def reset(self):
        Environment.reset(self)
        for g in self._stoch_groups:
            g.recalc()
