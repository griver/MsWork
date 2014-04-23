from fslib.env.environment import Environment
from fslib.env.point import Point


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