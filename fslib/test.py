# coding=utf-8
import fslib.util.fs_builder as FSBuilder
import fslib.util.env_builder as EnvBuilder
from fslib import ln

from fslib.util.plots import PlotBuilder


def show_curves(x_axis, func, *funcs):
    pb = PlotBuilder()
    pb.create_figure(1, 1)
    pb.plot_curves(0, x_axis, func, *funcs)
    pb.show()


def show_bars():
    pb = PlotBuilder()
    pb.create_figure(1, 1)
    bars = []
    bars.append(([ (50, 50), (150, 10) ], "first") )
    bars.append(([ (10, 50), (100, 20), (130, 10) ], "second"))
    pb.plot_bars(0, (0,200), (0, 40), 10, *bars)
    pb.show()


def line(n):
    env = EnvBuilder.line() #starting point (0)
    target = env.get_vertex(1) #point (1)
    net = FSBuilder.create_empty_network()
    motiv = FSBuilder.simple_motiv(env, target)
    act = FSBuilder.motor(env, net, 0, 1)
    #act = FSBuilder.lm_secondary2(env, motiv, env.get_vertex(0), target)
    net.add_motiv(motiv)
    net.add_motor(act)
    s = []
    r = []
    c = []
    ii = []
    ia = []
    ar = []

    for i in range(0, n):
        if i == 140:
            pass
        net.recalc()
        net.apply()
        s.append(act.get_S())
        r.append(act.get_R())
        c.append(act.get_C())  # * FSBuilder.act_gamma)
        ii.append(act._I)
        ia.append(act.get_IA())  # * FSBuilder.act_alpha)

    pb = PlotBuilder()
    pb.create_figure(1, 1)
    pb.plot_curves(0, range(0, n), (s, '-', 'S'), (r, '-', 'R'), (c, ':', 'C'), (ia, ':', 'IA'))
    pb.show()
    #pl.savefig('single act_fs.png')


def base(n):
    env = EnvBuilder.direct_square()
    target = env.get_vertex(3)
    net = FSBuilder.create_empty_network()
    #motiv = FSBuilder.simple_motiv(env, target)
    motiv = FSBuilder.motiv(env, target)
    #fs = FSBuilder.base_fs(env, motiv, 0, 1)
    fs = motiv
    net.add_motiv(motiv)
    #net.add_motor(fs)

    s = []
    r = []
    ii = []
    ia = []
    ar = []

    for i in range(0, n):

        net.recalc()
        net.apply()
        s.append(fs.get_S())
        r.append(fs.get_R())
        ia.append(fs.get_IA())
        ar.append(fs.get_AR())
        ii.append(fs.get_I())
        #print("fs.S = ", fs.get_S())

    pb = PlotBuilder()
    pb.create_figure(1, 1)
    pb.plot_curves(0, range(0, n),
                    (s, '-', 'S'),
                    (r, '-', 'R'),
                    (ia, '--', 'IA'),
                    (ar, '--', 'AR'),
                    (ii, '-', 'I'))
    pb.show()


def secondary(n):
    env = EnvBuilder.direct_square()
    target = env.get_vertex(3)
    net = FSBuilder.create_empty_network()
    motiv = FSBuilder.simple_motiv(env, target)
    #fs = FSBuilder.base_fs(env, motiv, 0, 1)

    fs = FSBuilder.secondary(env, motiv, env.get_vertex(0), env.get_vertex(1))
    net.add_motiv(motiv)
    net.add_vertex(fs)

    s = []
    r = []
    ia = []
    ar = []

    for i in range(0, n):
        net.recalc()
        net.apply()
        s.append(fs.get_S())
        r.append(fs.get_R())
        ia.append(fs.get_IA())
        ar.append(fs.get_AR())
        #print("fs.S = ", fs.get_S())

    pb = PlotBuilder()
    pb.create_figure(1, 1)
    pb.plot_curves(0, range(0, n), (s, 'b-', 'S'), (r, 'k-', 'R'), (ia, 'g--', 'IA'), (ar, 'r--', 'AR'))
    pb.show()


def direct_square(n):
    env = EnvBuilder.direct_square() #starting point (0,0)
    target = env.get_vertex(3) #point (1,1)
    net = FSBuilder.create_empty_network()
    motiv = FSBuilder.simple_motiv(env, target)
    act01 = FSBuilder.motor(env, net, 0, 1)
    act11 = FSBuilder.motor(env, net, 1, 1)

    net.add_motiv(motiv)
    net.add_motor(act01)
    net.add_motor(act11)

    slist1 = []
    slist0 = []
    for  i in range(0, n):
        net.recalc()
        net.apply()
        actList = net.get_actions()
        if len(actList) > 1:
            raise ValueError("Одновременно активны несколько FS действия")
        if len(actList) == 1:
            print(actList[0].name + " is active")
            env.update_state(actList[0])

        slist0.append(act01.get_S())
        slist1.append(act11.get_S())

    pb = PlotBuilder()
    pb.create_figure(1, 1)
    pb.plot_curves(0, range(0,n), (slist0, 'ro-', act01.name), (slist1, 'go-', act11.name))
    pb.show()


def square(n):
    env = EnvBuilder.square() #starting point (0,0)
    target = env.get_vertex(3) #point (1,1)
    net = FSBuilder.create_empty_network()
    motiv = FSBuilder.simple_motiv(env, target)
    act00 = FSBuilder.motor(env, net, 0, 0)
    act01 = FSBuilder.motor(env, net, 0, 1)
    act10 = FSBuilder.motor(env, net, 1, 0)
    act11 = FSBuilder.motor(env, net, 1, 1)

    net.add_motiv(motiv)
    net.add_motor(act00)
    net.add_motor(act01)
    net.add_motor(act10)
    net.add_motor(act11)

    slist0 = []
    slist1 = []
    slist2 = []
    slist3 = []

    for  i in range(0, n):
        net.recalc()
        net.apply()
        actList = net.get_actions()
        if len(actList) > 1:
            raise ValueError("Одновременно активны несколько FS действия")
        if len(actList) == 1:
            print(actList[0].name + " is active")
            env.update_state(actList[0])

        slist0.append(act00.get_S())
        slist1.append(act01.get_S())
        slist2.append(act10.get_S())
        slist3.append(act11.get_S())

    #pl.savefig('two act_fs S.png')
    show_curves(range(0,n),
              (slist0, 'r-', act00.name),
              (slist1, 'g-', act01.name),
              (slist2, 'b-', act10.name),
              (slist3, 'y-', act11.name)
    )


def cube(n):
    env = EnvBuilder.cube() #starting point (0,0,0)
    target = env.get_vertex(7) #point (1,1,1)
    net = FSBuilder.create_empty_network()

    motiv = FSBuilder.simple_motiv(env, target)
    act00 = FSBuilder.motor(env, net, 0, 0)
    act01 = FSBuilder.motor(env, net, 0, 1)
    act10 = FSBuilder.motor(env, net, 1, 0)
    act11 = FSBuilder.motor(env, net, 1, 1)
    act20 = FSBuilder.motor(env, net, 2, 0)
    act21 = FSBuilder.motor(env, net, 2, 1)

    net.add_motiv(motiv)
    net.add_motor(act00)
    net.add_motor(act01)
    net.add_motor(act10)
    net.add_motor(act11)
    net.add_motor(act20)
    net.add_motor(act21)

    slist1 = []
    slist2 = []
    slist3 = []
    slist4 = []
    slist5 = []
    slist6 = []

    prev = None
    for  i in range(0, n):
        net.recalc()
        net.apply()
        actList = net.get_actions()
        if len(actList) > 1:
            raise ValueError("Одновременно активны несколько FS действия")
        elif len(actList) == 1:
            if actList[0] is not prev:
                print(actList[0].name + " is active")
                prev = actList[0]
            env.update_state(actList[0])
        else:
            prev = None

        slist1.append(act00.get_S())
        slist2.append(act01.get_S())
        slist3.append(act10.get_S())
        slist4.append(act11.get_S())
        slist5.append(act20.get_S())
        slist6.append(act21.get_S())
    #pl.savefig('two act_fs S.png')
    show_curves(range(0,n),
              (slist1, 'r-', act00.name),
              (slist2, 'g-', act01.name),
              (slist3, 'b-', act10.name),
              (slist4, 'y-', act11.name),
              (slist5, 'c-', act20.name),
              (slist6, 'k-', act21.name)
    )


def fight(n, k = None):
    if k is None:
        k = int(input("Введите число конкурирующих систем: "))

    env = EnvBuilder.line()
    target = env.get_vertex(1)
    net = FSBuilder.create_empty_network()
    motiv = FSBuilder.simple_motiv(env, target)
    net.add_motiv(motiv)

    acts  = []
    s = []
    lines = []
    #net.create_cnet("MOTOR", 1.5)

    for i in range(0, k):
        act = FSBuilder.motor(env, net, 0, 1)
        #act = FSBuilder.lm_secondary(net, env, motiv, env.get_vertex(0), target)
        #act = FSBuilder.motiv(env, target)
        act.name = "act"+ str(i+1)
        #net.add_motor(act)
        net.add_in_cnet(act, "MOTOR")
        acts.append(act)
        s.append([])
        lines.append((s[i], '-', act.name))

    for  i in range(0, n):
        net.recalc()
        net.apply()
        for j in range(0, k):
            s[j].append(acts[j].get_S())

    show_curves(range(0,n), *lines)


def sec_influence_test(n, k = None):
    if k is None:
        k = int(input("Введите число конкурирующих систем: "))

    env = EnvBuilder.line()
    target = env.get_vertex(1)
    net = FSBuilder.create_empty_network("network_with_secondary_fs")
    motiv = FSBuilder.simple_motiv(env, target)
    net.add_motiv(motiv)
    #sec = FSBuilder.secondary(env, motiv, env.get_current_state(), target)
    sec = FSBuilder.lm_secondary(net, env, motiv, env.get_current_state(), target)
    sec.name = "secondary"
    sec._active_threshold = 2.0
    net.add_vertex(sec)

    acts  = []
    s = []
    sec_s = []
    lines = []
    for i in range(0, k):
        act = FSBuilder.motor(env, net, 0, 1)
        #act._active_threshold = 2.0
        act.name = "act"+ str(i+1)
        net.add_motor(act)
        acts.append(act)
        s.append([])
        lines.append((s[i], '--', act.name))

    for fs in net.all_motor():
        if fs is acts[0]:
            net.add_edge(sec, fs, 1.5)
        else:
            net.add_edge(sec, fs, -1.5)

    #net.write_to_file()
    for i in range(0, n):
        net.recalc()
        net.apply()
        for j in range(0, k):
            s[j].append(acts[j].get_S())
        sec_s.append(sec.get_S())

    tmp = net.get_action()

    show_curves(range(0, n), (sec_s, 'o--', sec.name), *lines)
    #return tmp[0] == acts[0]


def secondary_influence(n, iter, system_number):
    win = 0
    loose = 0
    for i in range(0, n):
        if sec_influence_test(iter, system_number):
            win += 1
        else:
            loose += 1
    print("Побед: " + str(win))
    print("Пордажений: " + str(loose))


def single_learning(goal_coordinates, env=EnvBuilder.cube()):

    sec_cnet_weight = 1.0
    sec_motiv_weight = 1.5
    net = FSBuilder.create_network(env, FSBuilder.motor, "base_network")

    assert isinstance(env, ln.Environment)
    assert isinstance(net, ln.BaseFSNetwork)

    target = env.get_state_by_coords(goal_coordinates)
    motiv = FSBuilder.simple_motiv(env, target)
    net.add_motiv(motiv)

    logger = ln.TrialLogger()
    #i = 0
    while True:
        print("----------------------------------------------------")
        ln.trial(net, env, logger)
        ln.network_update(net, env, logger, sec_cnet_weight, sec_motiv_weight)

        #i += 1
        #print(i)
        #if i > 30:
        ln.draw_trial(net, env, logger)
        if ln.exit_condition(): break

        ln.reset(net, env, logger)
        print("----------------------------------------------------")
    #net.write_to_file("learned_graph.dot")


def multi_learning(goals_coordinates, env=EnvBuilder.slingshot()):
    sec_cnet_weight = 1.0
    sec_motiv_weight = 1.5
    net = FSBuilder.create_network(env, FSBuilder.motor, "base_network")

    assert isinstance(env, ln.Environment)
    assert isinstance(net, ln.BaseFSNetwork)

    for t in goals_coordinates:
        target = env.get_state_by_coords(t)
        motiv = FSBuilder.motiv(env, target)
        net.add_motiv(motiv)

    logger = ln.TrialLogger()
    i = 0
    while True:
        i+=1
        print("----------------------------------------------------")
        ln.trial(net, env, logger)
        ln.network_update(net, env, logger, sec_cnet_weight, sec_motiv_weight)
        ln.reset(net)
        if not i % 5:
            #ln.draw_trial(net, env, logger)
            ln.draw_trial_bars(net, env, logger)
            if ln.exit_condition(): break
        print("----------------------------------------------------")


def stochastic_fork_test(n=1000):
    env, e1, e2 = EnvBuilder.fork()
    l1 = []
    l2 = []
    for i in range(0, n):
        env.reset()
        e1.is_available()
        l1.append(e1.is_available())
        l2.append(e2.is_available())
        if l1[i] + l2[i] != 1:
            print("Все работает неправильно!")

    s1 = reduce(lambda x, y: x + y, l1, 0)
    s2 = reduce(lambda x, y: x + y, l2, 0)
    print(s1)
    print(s2)
    print(s1+s2)

#--------------trash---------------------------------------------
import numpy as np

def logg(step, result):
        if step:
            print("go th the right")
        else:
            print("go th the left")

        if result == False:
            print("FAIl :(")
        else:
            print("WIN :(")

def get_list(n, p):
    return np.random.randint(1, 11, n) <= p

def direct_actor_test(e, r, ml, mr, array):
    is_right = False
    acts = [0.0,0.0]
    all_acts = 0.0
    log = []
    log.append([])
    log.append([])

    st = []
    for i in range(0, len(array)):
        if mr == ml:
            is_right = np.random.rand() > 0.5
        else:
            is_right =  mr > ml

        st.append(is_right)
        all_acts += 1.0
        q = (is_right == array[i])
        acts[is_right] += 1.0
        mr = mr + e*(is_right - acts[1]/float(all_acts) ) * (q - r)
        ml = ml + e*((not is_right) - acts[0]/float(all_acts) ) * (q - r)
        log[0].append(ml)
        log[1].append(mr)
        r += 1/all_acts * (q - r)
        logg(is_right, q)

        if q == False:
            print("Then:")
            is_right = not is_right

            all_acts += 1.0
            q = (is_right == array[i])
            acts[is_right] += 1.0
            mr = mr + e*(is_right - acts[1]/float(all_acts) ) * (q - r)
            ml = ml + e*((not is_right) - acts[0]/float(all_acts) ) * (q - r)

            log[0].append(ml)
            log[1].append(mr)

            r += 1/all_acts * (q - r)
            logg(is_right, q)

        print("acts:" + str(acts))
        print("r=" + str(r) +  "  ml=" + str(ml) + "  mr=" + str(mr))
        print("------------------------------------------------------")

    show_curves(range(0,len(log[0])),
              (log[0], 'r-', "left"),
              (log[1], 'b-', "right")
    )

    right = sum(st) / float(len(st))
    print("right first probability: " + str(right))
    print("left first probability: " + str(1.0 - right))
#--------------/trash---------------------------------------------

if __name__ == "__main__":
    #stochastic_fork_test(10000)

    #line(200)
    #base(300)
    #fight(800, 4)
    #secondary(200)
    single_learning((1, 1, 1), EnvBuilder.rhomb())
    #multi_learning([(0, 0, 0), (0, 0, 1), (1, 0, 0)])
    #sec_influence_test(200, 8)
    #line(200)
    #actor_test(0.01, 10.0 ,10.0, 10.0, get_list(10000, 9), )

else:
    pass

