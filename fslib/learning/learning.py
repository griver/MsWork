# coding=utf-8
from fslib import BaseMotor, BaseSecondary
from fslib.util import fs_builder as FSBuilder
from fslib.util.plots import PlotBuilder


def _find_predicate(sec, start, end, motiv):
    assert isinstance(sec, BaseSecondary)
    return sec.IA_point() is start and sec.AR_point() is end and sec.get_motivation() is motiv

def _find_unlearned_transit(path, net, motiv):
    goal = motiv.get_goal()
    if goal is not path[-1]:
        raise ValueError("path must end with a goal state")

    secs = net.all_secondary()
    rng = range(0,len(path) - 1)
    rng.reverse()
    for i in rng:  # without last state, because last state is a goal state
        fs = next((s for s in secs if _find_predicate(s, path[i], path[i+1], motiv)), None)
        if fs is None:
            return i

    return None


def single_goal_learning(env, net, motiv, sec_to_sec_weight, sec_to_motor_weight = 1.5):
    target = motiv.get_goal()
    motor_list = net.all_motor()

    activefs = 0
    n = 0
    st_path = []
    act_path = []
    prev_fs = None
    st_path.append(env.get_current_state())

    logger = []
    state_changes = []
    for v in net.vertices():
        logger.append([])

    while env.get_current_state() is not target: #and n < 500:
        n += 1
        #if n % 100 == 0:
        #    print(n)
        net.recalc_all()
        net.apply_all()
        active_motor_fs = filter(lambda fs: fs.is_active(), motor_list)

        for i in range(0, len(net.vertices())):
            logger[i].append(net.get_vertex(i).get_S())

        if len(active_motor_fs) > 1:
            raise ValueError("Одновременно активны несколько FS действия")
        elif len(active_motor_fs) == 0:
            prev_fs = None
            state_changes.append(env.get_current_state().get_id())
            continue

        curr_fs = active_motor_fs[0]
        if curr_fs is not prev_fs:
            print(curr_fs.name + " is active")
            activefs += 1
            prev_fs = curr_fs

        env.update_state(curr_fs)
        state_changes.append(env.get_current_state().get_id())

        if env.get_current_state() is not st_path[-1]:
            st_path.append(env.get_current_state())
            act_path.append(curr_fs)

    #state_changes.append(target.get_id())
    #----show graphs-------------------
    print("active_fs == " + str(activefs))
    act_funcs = []
    sec_funcs = []
    for i in range(0, len(logger)):
        fs = net.get_vertex(i)
        if isinstance(fs, BaseMotor):
            act_funcs.append((logger[i], '-', fs.name))
        elif isinstance(fs, BaseSecondary):
            sec_funcs.append((logger[i], '--', fs.name))
    pb = PlotBuilder()
    if len(sec_funcs) > 0:
        pb.create_figure(3, 1)
        pb.plot_funcs(1, range(0, n), *act_funcs)
        pb.plot_funcs(2, range(0, n), *sec_funcs)
    else:
        pb.create_figure(2, 1)
        pb.plot_funcs(1, range(0, n), *act_funcs)
    pb.plot_funcs(0, range(0, n), (state_changes, 'o-', "State"))
    pb.show()
    #---/show graphs-------------------

    id = _find_unlearned_transit(st_path, net, motiv)
    if id is None:
        print("Весь путь от начального состояния до цели был выучен")
        return n, st_path, logger

    print("Добавляем вторичную фс для перехода из " + st_path[id].name + " в " + st_path[id + 1].name)
    print("она будет стимулировать активность системы  " + act_path[id].name)
    sec = FSBuilder.lm_secondary(env, motiv, st_path[id], st_path[id + 1])

    # find other secondary fs associated with this state
    secs = filter(lambda fs: fs.IA_point() is st_path[id], net.all_secondary())

    net.add_vertex(sec)

    if len(secs) == 1:
        cnet_name = "CNET" + st_path[id].name
        net.create_cnet(cnet_name, sec_to_sec_weight)
        print("create competitive network: " + cnet_name)
        net.add_in_cnet(sec, cnet_name)
        net.add_in_cnet(secs[0], cnet_name)
    elif len(secs) > 1:
        cnet_name = secs[0].get_cnet_name()
        net.add_in_cnet(sec, cnet_name)

    net.add_vertex(sec)
    for fs in motor_list:
        if fs is act_path[id]:
            net.add_edge(sec, fs, sec_to_motor_weight)
        else:
            net.add_edge(sec, fs, -sec_to_motor_weight)
    return n, st_path, logger



