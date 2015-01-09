from fslib.env.environment import Environment
from fslib.env.point import Point
from fslib.graph.edge import Edge
from fslib import StochasticEnvironment
from fslib.stochasticenv.stochastic_environment import random_array
import numpy as np

#--------Environments-------------------------------------------------------
def line():
    env = Environment(1, "line")
    p0 = Point((0,))
    p1 = Point((1,))
    env.add_vertex(p0)
    env.add_vertex(p1)
    env.add_edge(p0, p1, 1)
    env.set_current_state(p0)
    return env


def chain(n):
    env = Environment(1, "chain")
    p0 = Point((0,))
    p1 = Point((1,))
    env.add_vertex(p0)
    env.add_vertex(p1)
    env.add_edge(p0, p1, 1)
    env.set_current_state(p0)
    return env


def square():
    env = direct_square()
    v = env.vertices()
    env.add_edge(v[1], v[0], 1)
    env.add_edge(v[2], v[0], 1)
    env.add_edge(v[3], v[1], 1)
    env.add_edge(v[3], v[2], 1)
    return env


def direct_square():
    env = Environment(2, "square")
    p00 = Point((0, 0))
    p01 = Point((0, 1))
    p10 = Point((1, 0))
    p11 = Point((1, 1))

    env.add_vertex(p00)
    env.add_vertex(p01)
    env.add_vertex(p10)
    env.add_vertex(p11)

    env.add_edge(p00, p01, 1)
    env.add_edge(p00, p10, 1)
    env.add_edge(p01, p11, 1)
    env.add_edge(p10, p11, 1)
    env.set_current_state(p00)
    return env


def cube():
    env = Environment(3, "cube")
    points = []
    for x in [0,1]:
        for y in [0, 1]:
            for z in [0, 1]:
                p = Point((x, y, z))
                env.add_vertex(p)
                points.append(p)

    env.add_edge(points[0], points[1], 1)
    env.add_edge(points[0], points[4], 1)
    env.add_edge(points[0], points[2], 1)
    env.add_edge(points[2], points[6], 1)
    env.add_edge(points[2], points[3], 1)
    env.add_edge(points[3], points[7], 1)

    env.add_edge(points[1], points[0], 1)
    env.add_edge(points[4], points[0], 1)
    env.add_edge(points[2], points[0], 1)
    env.add_edge(points[6], points[2], 1)
    env.add_edge(points[3], points[2], 1)
    env.add_edge(points[7], points[3], 1)

    env.set_current_state(points[0])
    return env


def slingshot():
    env = Environment(3, "slingshot")

    points = []
    points.append(Point((0, 0, 0)))  # 0
    points.append(Point((0, 1, 0)))  # 1
    points.append(Point((1, 1, 0)))  # 2
    points.append(Point((0, 1, 1)))  # 3
    points.append(Point((1, 0, 0)))  # 4
    points.append(Point((0, 0, 1)))  # 5
    for p in points:
        env.add_vertex(p)

    env.add_edge(points[0], points[1], 1)
    env.add_edge(points[1], points[0], 1)
    env.add_edge(points[1], points[2], 1)
    env.add_edge(points[2], points[1], 1)
    env.add_edge(points[2], points[4], 1)
    env.add_edge(points[4], points[2], 1)
    env.add_edge(points[1], points[3], 1)
    env.add_edge(points[3], points[1], 1)
    env.add_edge(points[3], points[5], 1)
    env.add_edge(points[5], points[3], 1)

    env.set_current_state(points[0])
    return env
#--------/Environments-------------------------------------------------------


#--------Stochastic Environments-------------------------------------------------------
def fork():
    env = StochasticEnvironment(2, "Fork" , 0)
    points = [Point((0, 0)), Point((0, 1)), Point((1, 0))]

    for p in points:
        env.add_vertex(p)
    e1 = env.add_edge(points[0], points[1])
    e2 = env.add_edge(points[0], points[2])
    env.create_competetive_group([e1, e2])
    return env, e1, e2

def rhomb():
    env = StochasticEnvironment(3, "Rhomb" , 0)
    points = [Point((0, 0, 0)), # 0
              Point((0, 1, 0)), # 1
              Point((1, 1, 0)), # 2
              Point((0, 1, 1)), # 3
              Point((1, 1, 1))] # 4

    for p in points:
        env.add_vertex(p)
    env.add_edge(points[0], points[1])
    env.add_edge(points[1], points[2])
    env.add_edge(points[1], points[3])
    e1 = env.add_edge(points[2], points[4])
    e2 = env.add_edge(points[3], points[4])

    env.add_edge(points[1], points[0])
    env.add_edge(points[2], points[1])
    env.add_edge(points[3], points[1])

    env.create_competitive_group([e1, e2], (0.7, 0.3))
    return env

def binary_choice(left_prob):
    env = StochasticEnvironment(5, "BinaryChoice", 0)
    points = [Point((0, 0, 0, 0, 0)),  # 0
              Point((1, 0, 0, 0, 0)),  # 1
              Point((0, 0, 0, 0, 1)),  # 2
              Point((1, 1, 0, 0, 0)),  # 3
              Point((0, 0, 0, 1, 1)),  # 4
              Point((1, 1, 1, 0, 0)),  # 5
              Point((0, 0, 1, 1, 1)),  # 6
              Point((1, 1, 1, 1, 0)),  # 7
              Point((0, 1, 1, 1, 1)),  # 8
              Point((1, 1, 1, 1, 1))]  # 9

    for p in points:
        env.add_vertex(p)

    env.add_both_edges(points[0], points[1])
    env.add_both_edges(points[1], points[3])
    env.add_both_edges(points[3], points[5])
    env.add_both_edges(points[5], points[7])

    env.add_both_edges(points[0], points[2])
    env.add_both_edges(points[2], points[4])
    env.add_both_edges(points[4], points[6])
    env.add_both_edges(points[6], points[8])

    e1 = env.add_edge(points[7], points[9])
    e2 = env.add_edge(points[8], points[9])

    env.create_competetive_group([e1, e2], [left_prob, 1.0 - left_prob])
    return env

def stochastic_env1():
    env = StochasticEnvironment(4, "StochasticEnv1", 0)
    points = [Point((0, 0, 0, 0)),  # 0
              Point((0, 0, 0, 1)),  # 1
              Point((0, 1, 0, 1)),  # 2
              Point((0, 1, 0, 0)),  # 3
              Point((0, 1, 1, 0)),  # 4
              Point((0, 0, 1, 0)),  # 5
              Point((0, 0, 1, 1)),  # 6
              Point((0, 1, 1, 1)),  # 7
              Point((1, 1, 1, 1)),  # 8
              Point((1, 0, 1, 1)),  # 9
              Point((1, 1, 1, 0)),  # 10
              Point((1, 0, 1, 0))]  # 11

    for p in points:
        env.add_vertex(p)

    env.add_both_edges(points[0], points[1])  # 0 <-> 1 -> 2 <-> 7
    e1 = env.add_edge(points[1], points[2])
    env.add_both_edges(points[2], points[7])

    env.add_both_edges(points[0], points[3])  # 0 <-> 3 <-> 4 -> 7
    env.add_both_edges(points[3], points[4])
    e2 = env.add_edge(points[4], points[7])

    e3 = env.add_edge(points[0], points[5])  # 0 -> 5 <-> 6 <-> 7
    env.add_both_edges(points[5], points[6])
    env.add_both_edges(points[6], points[7])

    env.add_both_edges(points[7], points[8])  # 7 <-> 8

    env.add_both_edges(points[8], points[10])  # 8 <-> 10 -> 11
    e4 = env.add_edge(points[10], points[11])

    e5 = env.add_edge(points[8], points[9])  # 8 -> 9 <-> 11
    env.add_both_edges(points[9], points[11])

    env.create_competetive_group([e1, e2, e3])
    env.create_competetive_group([e4, e5])
    return env


def stochastic_env2(left_prob):
    env = StochasticEnvironment(2, "StochasticEnv1", 0)
    points = [Point((0, 0)),  # 0
              Point((0, 1)),  # 1
              Point((1, 0)),  # 2
              Point((1, 1))]  # 3

    for p in points:
        env.add_vertex(p)

    e1 = env.add_edge(points[0], points[1])
    env.add_edge(points[1], points[3])

    e2 = env.add_edge(points[0], points[2])
    env.add_edge(points[2], points[3])

    env.create_competetive_group([e1, e2], [left_prob, 1.0 - left_prob])
    return env

def grid33():
    env = StochasticEnvironment(4, "StochasticEnv1", 1)
    points = [Point((1, 0, 0, 0)),  # 0
              Point((0, 0, 0, 0)),  # 1
              Point((0, 0, 0, 1)),  # 2
              Point((1, 1, 0, 0)),  # 3
              Point((0, 1, 0, 0)),  # 4
              Point((0, 1, 0, 1)),  # 5
              Point((1, 1, 1, 0)),  # 6
              Point((0, 1, 1, 0)),  # 7
              Point((0, 1, 1, 1))]  # 8

    for p in points:
        env.add_vertex(p)

    env.add_both_edges(points[0], points[1])
    env.add_both_edges(points[1], points[2])
    e1 = env.add_edge(points[0], points[3])
    e2 = env.add_edge(points[1], points[4])
    e3 = env.add_edge(points[2], points[5])

    env.add_both_edges(points[3], points[4])
    env.add_both_edges(points[4], points[5])
    e4 = env.add_edge(points[3], points[6])
    e5 = env.add_edge(points[4], points[7])
    e6 = env.add_edge(points[5], points[8])

    env.add_both_edges(points[6], points[7])
    env.add_both_edges(points[7], points[8])

    return env, [e1,e2, e3], [e4, e5, e6]

def torus(x, y, get_probabilities=None):

    size = int(np.ceil(np.log2(x*y)))
    binary =  '{0:0' + str(size) + 'b}'
    env = StochasticEnvironment(size, "torus", 0)
    points = np.empty((x, y), dtype=Point)
    edges = []

    for i in xrange(x):
        for j in xrange(y):
            points[i][j] = Point(tuple(binary.format(i*y + j)))
            env.add_vertex(points[i][j])

    for i in xrange(x):
        for j in xrange(y):
            e1e2 = env.add_both_edges(points[i][j], points[i][(j + 1) % y])  # right
            edges.append(e1e2)
            e1e2 = env.add_both_edges(points[i][j], points[(i + 1) % x][j])  # bottom
            edges.append(e1e2)

    """ for i in xrange(x):
        for j in xrange(y): # add outcoming edges in clockwise order starting from the top
            edges.append( env.add_edge(points[i][j], points[(i - 1) % x][j]) )  # top       0
            edges.append( env.add_edge(points[i][j], points[i][(j + 1) % y]) ) # right     1
            edges.append( env.add_edge(points[i][j], points[(i + 1) % x][j]) ) # bottom    2
            edges.append( env.add_edge(points[i][j], points[i][(j - 1) % y]) )  # left      3 """

    if get_probabilities is None:
        return env

    probs = get_probabilities(len(edges))
    for i in xrange(len(edges)):
        env.create_united_group( edges[i], probs[i])
    return env


def scc_sample():

    size = int(np.ceil(np.log2(12)))
    binary = '{0:0' + str(size) + 'b}'
    p = np.empty(12, dtype=Point)

    env = StochasticEnvironment(size, "scc_sample", 0)

    for i in xrange(12):
        p[i] = Point(tuple(binary.format(i)))
        env.add_vertex(p[i])

    env.add_edge(p[0], p[1])

    env.add_edge(p[1], p[2])
    env.add_edge(p[1], p[4])
    env.add_edge(p[1], p[3])

    env.add_edge(p[2], p[5])

    env.add_edge(p[4], p[1])
    env.add_edge(p[4], p[5])
    env.add_edge(p[4], p[6])

    env.add_edge(p[5], p[2])
    env.add_edge(p[5], p[7])

    env.add_edge(p[6], p[7])
    env.add_edge(p[6], p[9])

    env.add_edge(p[7], p[10])

    env.add_edge(p[8], p[6])

    env.add_edge(p[9], p[8])

    env.add_edge(p[10], p[11])

    env.add_edge(p[11], p[9])

    return env

#--------/Stochastic Environments-------------------------------------------------------
#--------/Stochastic Environments-------------------------------------------------------

