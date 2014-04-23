# coding=utf-8
import fslib.util.fs_builder as FSBuilder
import fslib.util.env_builder as EnvBuilder
from fslib import ln

from fslib.util.plots import PlotBuilder

def show_plot(x_axis, func, *funcs):
    pb = PlotBuilder()
    pb.create_figure(1, 1)
    pb.plot_funcs(0, x_axis, func, *funcs)
    pb.show()


def line(n):
    env = EnvBuilder.line() #starting point (0)
    target = env.get_vertex(1) #point (1)
    net = FSBuilder.base_network()
    motiv = FSBuilder.simple_motiv(env, target)
    act = FSBuilder.motor(env, motiv, 0, 1)
    #act = FSBuilder.lm_secondary2(env, motiv, env.get_vertex(0), target)
    net.add_vertex(motiv)
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
        net.recalc_all()
        net.apply_all()
        s.append(act.get_S())
        r.append(act.get_R())
        c.append(act.get_C())  # * FSBuilder.act_gamma)
        ii.append(act._I)
        ia.append(act.get_IA())  # * FSBuilder.act_alpha)

    pb = PlotBuilder()
    pb.create_figure(1, 1)
    pb.plot_funcs(0, range(0, n), (s, '-', 'S'), (r, '-', 'R'), (c, ':', 'C'), (ia, ':', 'IA'))
    pb.show()
    #pl.savefig('single act_fs.png')


def base(n):
    env = EnvBuilder.direct_square()
    target = env.get_vertex(3)
    net = FSBuilder.base_network()
    #motiv = FSBuilder.simple_motiv(env, target)
    motiv = FSBuilder.motiv(env, target)
    #fs = FSBuilder.base_fs(env, motiv, 0, 1)
    fs = motiv
    net.add_vertex(motiv)
    #net.add_motor(fs)

    s = []
    r = []
    ii = []
    ia = []
    ar = []

    for i in range(0, n):

        net.recalc_all()
        net.apply_all()
        s.append(fs.get_S())
        r.append(fs.get_R())
        ia.append(fs.get_IA())
        ar.append(fs.get_AR())
        ii.append(fs.get_I())
        #print("fs.S = ", fs.get_S())

    pb = PlotBuilder()
    pb.create_figure(1, 1)
    pb.plot_funcs(0, range(0, n),
                    (s, '-', 'S'),
                    (r, '-', 'R'),
                    (ia, '--', 'IA'),
                    (ar, '--', 'AR'),
                    (ii, '-', 'I'))
    pb.show()


def secondary(n):
    env = EnvBuilder.direct_square()
    target = env.get_vertex(3)
    net = FSBuilder.base_network()
    motiv = FSBuilder.simple_motiv(env, target)
    #fs = FSBuilder.base_fs(env, motiv, 0, 1)

    fs = FSBuilder.secondary(env, motiv, env.get_vertex(0), env.get_vertex(1))
    net.add_vertex(motiv)
    net.add_vertex(fs)

    s = []
    r = []
    ia = []
    ar = []

    for i in range(0, n):
        net.recalc_all()
        net.apply_all()
        s.append(fs.get_S())
        r.append(fs.get_R())
        ia.append(fs.get_IA())
        ar.append(fs.get_AR())
        #print("fs.S = ", fs.get_S())

    pb = PlotBuilder()
    pb.create_figure(1, 1)
    pb.plot_funcs(0, range(0, n), (s, 'b-', 'S'), (r, 'k-', 'R'), (ia, 'g--', 'IA'), (ar, 'r--', 'AR'))
    pb.show()


def direct_square(n):
    env = EnvBuilder.direct_square() #starting point (0,0)
    target = env.get_vertex(3) #point (1,1)
    net = FSBuilder.base_network()
    motiv = FSBuilder.simple_motiv(env, target)
    act01 = FSBuilder.motor(env, motiv, 0, 1)
    act11 = FSBuilder.motor(env, motiv, 1, 1)

    net.add_vertex(motiv)
    net.add_motor(act01)
    net.add_motor(act11)

    slist1 = []
    slist0 = []
    for  i in range(0, n):
        net.recalc_all()
        net.apply_all()
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
    pb.plot_funcs(0, range(0,n), (slist0, 'ro-', act01.name), (slist1, 'go-', act11.name))
    pb.show()


def square(n):
    env = EnvBuilder.square() #starting point (0,0)
    target = env.get_vertex(3) #point (1,1)
    net = FSBuilder.base_network()
    motiv = FSBuilder.simple_motiv(env, target)
    act00 = FSBuilder.motor(env, motiv, 0, 0)
    act01 = FSBuilder.motor(env, motiv, 0, 1)
    act10 = FSBuilder.motor(env, motiv, 1, 0)
    act11 = FSBuilder.motor(env, motiv, 1, 1)

    net.add_vertex(motiv)
    net.add_motor(act00)
    net.add_motor(act01)
    net.add_motor(act10)
    net.add_motor(act11)

    slist0 = []
    slist1 = []
    slist2 = []
    slist3 = []

    for  i in range(0, n):
        net.recalc_all()
        net.apply_all()
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
    show_plot(range(0,n),
              (slist0, 'r-', act00.name),
              (slist1, 'g-', act01.name),
              (slist2, 'b-', act10.name),
              (slist3, 'y-', act11.name)
    )


def cube(n):
    env = EnvBuilder.cube() #starting point (0,0,0)
    target = env.get_vertex(7) #point (1,1,1)
    net = FSBuilder.base_network()

    motiv = FSBuilder.simple_motiv(env, target)
    act00 = FSBuilder.motor(env, motiv, 0, 0)
    act01 = FSBuilder.motor(env, motiv, 0, 1)
    act10 = FSBuilder.motor(env, motiv, 1, 0)
    act11 = FSBuilder.motor(env, motiv, 1, 1)
    act20 = FSBuilder.motor(env, motiv, 2, 0)
    act21 = FSBuilder.motor(env, motiv, 2, 1)

    net.add_vertex(motiv)
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
        net.recalc_all()
        net.apply_all()
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
    show_plot(range(0,n),
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
    net = FSBuilder.base_network()
    motiv = FSBuilder.simple_motiv(env, target)

    acts  = []
    s = []
    lines = []
    net.create_cnet("MOTOR", 1.5)

    for i in range(0, k):
        #act = FSBuilder.motor(env, motiv, 0, 1)
        #act = FSBuilder.lm_secondary(env, motiv, env.get_vertex(0), target)
        act = FSBuilder.motiv(env, target)
        act.name = "act"+ str(i+1)
        #net.add_motor(act)
        net.add_in_cnet(act, "MOTOR")
        acts.append(act)
        s.append([])
        lines.append((s[i], '-', act.name))

    for  i in range(0, n):
        net.recalc_all()
        net.apply_all()
        for j in range(0, k):
            s[j].append(acts[j].get_S())

    show_plot(range(0,n), *lines)


def sec_influence_test(n, k = None):
    if k is None:
        k = int(input("Введите число конкурирующих систем: "))

    env = EnvBuilder.line()
    target = env.get_vertex(1)
    net = FSBuilder.base_network("with_sec_fs_net")
    motiv = FSBuilder.simple_motiv(env, target)
    #sec = FSBuilder.secondary(env, motiv, env.get_current_state(), target)
    sec = FSBuilder.lm_secondary(env, motiv, env.get_current_state(), target)
    sec.name = "secondary"
    sec._active_threshold = 2.0
    net.add_vertex(sec)

    acts  = []
    s = []
    sec_s = []
    lines = []
    for i in range(0, k):
        act = FSBuilder.motor(env, motiv, 0, 1)
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
        net.recalc_all()
        net.apply_all()
        for j in range(0, k):
            s[j].append(acts[j].get_S())
        sec_s.append(sec.get_S())

    tmp = net.get_actions()
    if len(tmp) > 1:
        raise AssertionError("Беда! Несколько подбедителей среди MotorFS!")
    show_plot(range(0, n), (sec_s, 'o--', sec.name), *lines)
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


def learning_test():
    env = EnvBuilder.cube()
    net = FSBuilder.base_network("base_network")

    target = env.get_vertex(7)
    motiv = FSBuilder.simple_motiv(env, target)

    act00 = FSBuilder.motor(env, motiv, 0, 0)
    act01 = FSBuilder.motor(env, motiv, 0, 1)
    act10 = FSBuilder.motor(env, motiv, 1, 0)
    act11 = FSBuilder.motor(env, motiv, 1, 1)
    act20 = FSBuilder.motor(env, motiv, 2, 0)
    act21 = FSBuilder.motor(env, motiv, 2, 1)

    net.add_vertex(motiv)
    net.add_motor(act00)
    net.add_motor(act01)
    net.add_motor(act10)
    net.add_motor(act11)
    net.add_motor(act20)
    net.add_motor(act21)


    while True:
        print("----------------------------------------------------")
        n, path, log = ln.single_goal_learning(env, net, motiv, 1.0)
        net.reset_all()
        env.set_current_state(env.get_vertex(0))

        tmp = int(input("Хотите продолжить обучение? (1/ 0)\n"))

        if tmp == 0:
            break


if __name__ == "__main__":
    #line(200)
  #  base(300)
  #  fight(800, 4)
    #secondary(200)
    learning_test()

    #sec_influence_test(200, 8)
    #line(200)
    #learning_test()

else:
    pass

