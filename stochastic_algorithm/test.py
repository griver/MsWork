# coding=utf-8
from fslib.test import *
from stochastic_algorithm.fs import build_fast_motor
from stochastic_algorithm.learning import stochastic_learning as sln
from stochastic_algorithm.learning import td_learning as tdl
from stochastic_algorithm.util import graph2dot as dot
from fslib import algo


def print_state_vf(keys, vf):
    for k in keys:
        if vf.has(k):
            print(str(k.get_id()) + " == " + str(vf.get(k)))


def print_action_vf(keys, vf):
    for k in keys:
        if vf.has(k):
            print(k.name + " == " + str(vf.get(k)))


def last_n_averages(values, n):
    l =[]
    for i in xrange(0, len(values)):
        part = values[max(0, i + 1 - n): i + 1]
        l.append(sum(part) / float(len(part)))
    return l


def weighted_average(values, alpha):
    wa = values[0]
    l =[]
    for i in xrange(0, len(values)):
        wa += alpha*(values[i] - wa)
        l.append(wa)
    return l


def calc_weighted_average_list(values, id, alpha):
    wa = 0.5
    l =[]
    for i in xrange(0, len(values)):
        wa += alpha*((values[i] == id) - wa)
        l.append(wa)
    return l


def old_stoch_learning(goal_coordinates, env, vf=None, av=None):
    """
    Старая версия функции stoch_learning

    """
    #env, elist1, elist2 = EnvBuilder.grid33()
    #env.create_competetive_group(elist1, [.6, .2, .2])
    #env.create_competetive_group(elist2, [.2, .2, .6])

    #goal_coordinates = (0,1,1,0)
    if vf is None: vf = sln.ValueFunction()
    if av is None: av = sln.ValueFunction()

    sec_cnet_weight = 1.0
    sec_motiv_weight = 1.5
    net = FSBuilder.create_network(env, FSBuilder.motor, "base_network")

    assert isinstance(env, ln.Environment)
    assert isinstance(net, ln.BaseFSNetwork)

    target = env.get_state_by_coords(goal_coordinates)
    motiv = FSBuilder.simple_motiv(env, target)
    net.add_motiv(motiv)

    logger = sln.SecondaryLogger()
    if not vf.has(target):
        vf.put(target, 1.0)
    """stats1 = Statisitcs([(env.get_vertex(0), env.get_vertex(3)),
                         (env.get_vertex(1), env.get_vertex(4)),
                         (env.get_vertex(2), env.get_vertex(5))],
                        ["edge1", "edge2","edge3"])

    stats2 = Statisitcs([(env.get_vertex(3), env.get_vertex(6)),
                         (env.get_vertex(4), env.get_vertex(7)),
                         (env.get_vertex(5), env.get_vertex(8))],
                        ["edge4", "edge5","edge6"])  # """

    stats1 = sln.ChoiceStatistic([(env.get_vertex(0), env.get_vertex(1)),
                         (env.get_vertex(0), env.get_vertex(2))],
                        ["path1", "path2"]) # """

    i = 0
    while True:
        print("----------------------------------------------------")

        ln.trial(net, env, logger)
        ln.network_update(net, env, logger, sec_cnet_weight, sec_motiv_weight)

        i += 1

        #vf.add_if_absent(map(lambda s: s.IA_point() ,net.all_secondary()), 0.5)
        vf.add_if_absent(net.all_secondary(), 0.5)
        av.add_if_absent(net.all_secondary(), 10.0)

        sln.calc_action_value_function(logger, vf, av, net, 0.05, 0.01, 1.0, 0.0)
        sln.update_weights(net, vf)

        stats1.check_statistic(logger)
        #stats2.check_statistic(logger)
        #dot.state_value_function2dot(net, vf, "state_values.dot")
        print("-----------STEP!!!!------------------------------------------")
        print(i)

        #if i % 200 == 0:
        #print("-----------value_function_part------------------------------------------")
        #print_state_vf(env.vertices(), vf)
        #print("-----------/value_function_part------------------------------------------")
        #print("-----------action_values_part------------------------------------------")
        #print_action_vf(net.all_secondary(), av)
        #print("-----------/action_values_part------------------------------------------")
        print("Trial history_length: + " + str(len(logger.trial_history)) )
        ln.draw_trial(net, env, logger)
        stats1.print_stat(200)
        #stats2.print_stat(200)
        #stats.clear()
        if ln.exit_condition():
        #vf = mark_good_and_bad_secondary(logger)
            #vf2 = mark_error_decay_secondary(logger, net)
            #dot.secondary_graph2dot(net, vf2, "error_decay_secs.dot")
            break

        ln.reset(net, env, logger)
        print("----------------------------------------------------")

        if i == 1000:
            e1 = env.get_vertex(9).get_incoming()[0]  #  env.get_vertex(1).get_incoming()[0] #
            e2 = env.get_vertex(9).get_incoming()[1]  #  env.get_vertex(2).get_incoming()[0]
            env.remove_stochasticity()
            env.set_probability_to_edges([e1, e2], [0.3, 0.7])


    lwa = calc_weighted_average_list(stats1.list, 0, 0.01)
    rwa = calc_weighted_average_list(stats1.list, 1, 0.01)
    show_curves(range(0, len(lwa)), (lwa, "-", "left turn first"),(rwa, "-", "right turn first"))
    #net.write_to_file("learned_graph.dot")
    return net, vf, av


def create_complex_trial_sample():
    """
    Fake trial sample to check propagation of the prediction error in stochastic algorithm
    """

    env = EnvBuilder.Environment(1, "FakeEnvForTrialSample")
    p = []
    for i in xrange(0, 22):
        p.append(EnvBuilder.Point(i))
        env.add_vertex(p[-1])

    net = FSBuilder.create_network(env, FSBuilder.motor, "FakeNetForTrialSample")
    assert isinstance(net, FSBuilder.BaseFSNetwork)
    motiv = FSBuilder.simple_motiv(env, p[-1])
    net.add_motiv(motiv)

    secs = []
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[0], p[1]))
    net.add_vertex(secs[-1])

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[1], p[2]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[1], p[3]))
    net.create_cnet("1", 1.0)
    net.add_in_cnet(secs[-1], "1")
    net.add_in_cnet(secs[-2], "1")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[2], p[15]))
    net.add_vertex(secs[-1])

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[6], p[4]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[6], p[5]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[6], p[7]))
    net.create_cnet("6", 1.0)
    net.add_in_cnet(secs[-1], "6")
    net.add_in_cnet(secs[-2], "6")
    net.add_in_cnet(secs[-3], "6")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[7], p[6]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[7], p[13]))
    net.create_cnet("7", 1.0)
    net.add_in_cnet(secs[-1], "7")
    net.add_in_cnet(secs[-2], "7")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[9], p[8]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[9], p[10]))
    net.create_cnet("9", 1.0)
    net.add_in_cnet(secs[-1], "9")
    net.add_in_cnet(secs[-2], "9")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[10], p[9]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[10], p[11]))
    net.create_cnet("10", 1.0)
    net.add_in_cnet(secs[-1], "10")
    net.add_in_cnet(secs[-2], "10")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[11], p[10]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[11], p[12]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[11], p[13]))
    net.create_cnet("11", 1.0)
    net.add_in_cnet(secs[-1], "11")
    net.add_in_cnet(secs[-2], "11")
    net.add_in_cnet(secs[-3], "11")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[13], p[11]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[13], p[7]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[13], p[14]))
    net.create_cnet("13", 1.0)
    net.add_in_cnet(secs[-1], "13")
    net.add_in_cnet(secs[-2], "13")
    net.add_in_cnet(secs[-3], "13")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[14], p[13]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[14], p[15]))
    net.create_cnet("14", 1.0)
    net.add_in_cnet(secs[-1], "14")
    net.add_in_cnet(secs[-2], "14")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[15], p[14]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[15], p[16]))
    net.create_cnet("15", 1.0)
    net.add_in_cnet(secs[-1], "15")
    net.add_in_cnet(secs[-2], "15")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[16], p[15]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[16], p[17]))
    net.create_cnet("16", 1.0)
    net.add_in_cnet(secs[-1], "16")
    net.add_in_cnet(secs[-2], "16")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[17], p[16]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[17], p[18]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[17], p[19]))
    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[17], p[20]))
    net.create_cnet("17", 1.0)
    net.add_in_cnet(secs[-1], "17")
    net.add_in_cnet(secs[-2], "17")
    net.add_in_cnet(secs[-3], "17")
    net.add_in_cnet(secs[-4], "17")

    secs.append(FSBuilder.lm_secondary2(net, env, motiv, p[20], p[21]))
    net.add_vertex(secs[-1])

    logger = sln.SecondaryLogger()
    th = logger.trial_history

    th.append(sln.TrialActionInfo(None, p[1], filter(lambda x: x.IA_point() == p[0] and x.AR_point() == p[1], secs)[0]))
    th.append(sln.TrialActionInfo(None, None, filter(lambda x: x.IA_point() == p[1] and x.AR_point() == p[3], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[2], filter(lambda x: x.IA_point() == p[1] and x.AR_point() == p[2], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[15], filter(lambda x: x.IA_point() == p[2] and x.AR_point() == p[15], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[14], filter(lambda x: x.IA_point() == p[15] and x.AR_point() == p[14], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[13], filter(lambda x: x.IA_point() == p[14] and x.AR_point() == p[13], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[7], filter(lambda x: x.IA_point() == p[13] and x.AR_point() == p[7], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[6], filter(lambda x: x.IA_point() == p[7] and x.AR_point() == p[6], secs)[0]))
    th.append(sln.TrialActionInfo(None, None, filter(lambda x: x.IA_point() == p[6] and x.AR_point() == p[4], secs)[0]))
    th.append(sln.TrialActionInfo(None, None, filter(lambda x: x.IA_point() == p[6] and x.AR_point() == p[5], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[7], filter(lambda x: x.IA_point() == p[6] and x.AR_point() == p[7], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[13], filter(lambda x: x.IA_point() == p[7] and x.AR_point() == p[13], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[11], filter(lambda x: x.IA_point() == p[13] and x.AR_point() == p[11], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[10], filter(lambda x: x.IA_point() == p[11] and x.AR_point() == p[10], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[9], filter(lambda x: x.IA_point() == p[10] and x.AR_point() == p[9], secs)[0]))
    th.append(sln.TrialActionInfo(None, None, filter(lambda x: x.IA_point() == p[9] and x.AR_point() == p[8], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[10], filter(lambda x: x.IA_point() == p[9] and x.AR_point() == p[10], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[11], filter(lambda x: x.IA_point() == p[10] and x.AR_point() == p[11], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[13], filter(lambda x: x.IA_point() == p[11] and x.AR_point() == p[13], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[14], filter(lambda x: x.IA_point() == p[13] and x.AR_point() == p[14], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[15], filter(lambda x: x.IA_point() == p[14] and x.AR_point() == p[15], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[16], filter(lambda x: x.IA_point() == p[15] and x.AR_point() == p[16], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[17], filter(lambda x: x.IA_point() == p[16] and x.AR_point() == p[17], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[20], filter(lambda x: x.IA_point() == p[17] and x.AR_point() == p[20], secs)[0]))
    th.append(sln.TrialActionInfo(None, p[21], filter(lambda x: x.IA_point() == p[20] and x.AR_point() == p[21], secs)[0]))

    vf = sln.mark_error_decay_secondary(logger, net)
    dot.secondary_graph2dot(net, vf, "fake_trial_mark_error_decay.dot")


def stoch_learning(goal_coordinates, env, trials_number=250, vf=None):
    sec_cnet_weight = 1.0   # вес связей между вторичными ФС
    sec_motor_weight = 1.5  # вес связи от вторичной ФС к моторной

    # vf - функция ценности определенная на вторичных FS
    if vf is None: vf = sln.ValueFunction()

    # Сеть функциональных систем. Сначала содержит только моторные ФС.
    net = FSBuilder.create_edge_moving_network(env,  build_fast_motor, "edge_moving_agent")  # FSBuilder.edge_moving_motor

    # Определяем целевое состояние в среде и создаем мотивационную ФС связанную с ним.
    target = env.get_state_by_coords(goal_coordinates)
    motiv = FSBuilder.simple_motiv(env, target)
    net.add_motiv(motiv)

    # logger сохраняет информацию по испытанию, включая путь и последовательность активаций вторичных ФС
    logger = sln.SecondaryLogger()

    # данные для подсчета статистики по результатам обучения:
    action_numbers = []  # список будет хранить число шагов в iом испытаний
    secondary_size = []  # список будет размер сети вторичных фс в iом испытании

    trials_complete = 0  # счетчик числа испытаний
    while True:
        res = algo.bfs(env, env.get_current_state(), target)  # поиском в ширину проверяем доступность цели.

        if res is None:  # если цель недоступна сообщаем и по новой разыгрываем доступность переходов в среде.
            print("В этот раз пути нет. Попробуем еще раз!")
            env.reset()
            continue
        print((res.coords(), res.get_id()))
        print("----------------------------------------------------")

        ln.trial(net, env, logger)  # испытание агента в среде. заканчивается когда агент достигает целевого состояния
        trials_complete += 1

        ln.network_update(net, env, logger, sec_cnet_weight, sec_motor_weight)  # если нужно расширяем слой вторичных фс

        vf.add_if_absent(net.all_secondary(), 0.5)  # определяем ценность по умолчанию для новых вторичных ФС
        sln.calc_action_value_function(logger, vf, net, 0.05, 1.0, 0.0)  # обновляем функцию ценности по истории испытания
        sln.update_weights(net, vf)  # обновляем веса между мотивацией и вторичными ФС на основе функции ценности

        action_numbers.append(len(logger.trial_history))
        secondary_size.append(len(net.all_secondary()))


        if not trials_complete % trials_number: # выход из цикла обучения
            #ln.draw_trial(net, env, logger)
            #if ln.exit_condition():
            break

        ln.reset(net, env, logger)  # обнуляем необходимые значения между испытаниями
        print("STEP:" + str(trials_complete))  # номер завершившегося испытания
        print("----------------------------------------------------")

    return action_numbers, secondary_size


def base_learning(goal_coordinates, env, trials_number=400):
    sec_cnet_weight = 1.0
    sec_motiv_weight = 1.5
    net = FSBuilder.create_edge_moving_network(env, FSBuilder.edge_moving_motor, "base_network")

    target = env.get_state_by_coords(goal_coordinates)
    motiv = FSBuilder.simple_motiv(env, target)
    net.add_motiv(motiv)

    logger = sln.SecondaryLogger()
    action_numbers = []
    i = 0

    while True:
        print("----------------------------------------------------")
        i += 1
        ln.trial(net, env, logger)
        ln.network_update(net, env, logger, sec_cnet_weight, sec_motiv_weight)
        action_numbers.append(len(logger.trial_history))

        if not i % trials_number:
            #ln.draw_trial(net, env, logger)
            #if ln.exit_condition():
            break

        ln.reset(net, env, logger)
        print("STEP:" + str(i))
        print("----------------------------------------------------")

    return action_numbers


def Q_learning_test(goal_coordinates, env, epsilon, alpha, gamma=1.0, reward=1.0, penalty=-1.0):
    strategy = tdl.epsilon_greedy_strategy(epsilon)
    algorithm = lambda en, vf, target: tdl.Q_learning(en, vf, target, strategy, alpha, gamma, reward, penalty)
    return tdl.td_learning(algorithm, goal_coordinates, env)


def SARSA_test(goal_coordinates, env, epsilon, alpha, gamma=1.0, reward=1.0, penalty=-1.0):
    strategy = tdl.epsilon_greedy_strategy(epsilon)
    algorithm = lambda en, vf, target: tdl.SARSA(en, vf, target, strategy, alpha, gamma, reward, penalty)
    return tdl.td_learning(algorithm, goal_coordinates, env)


def test_graph_statisics():
    discrete_random = lambda size: EnvBuilder.random_array([1., 0.3, 0.7], [0.25, 0.25, 0.5], size)

    probs = []
    for j in xrange(100):
        torus = EnvBuilder.torus(50, 50, EnvBuilder.np.random.random_sample)
        #dot.stoch_environment2dot(torus)
        print(j)
        result = 0
        end = (50/2)*50 + 50/2
        get_incoming = lambda v: [e.get_src() for e in v.get_incoming() if e.is_available()]

        for i in xrange(100):
            """scc = algo.strong_connected_components(torus)
            for s in scc:
                if torus.vertices()[end] in s:
                    result += len(s) """
            #result += 0 if algo.bfs(torus, torus.vertices()[0], torus.vertices()[end]) is None else 1
            visit = set()
            algo.dfs_explore(torus, torus.vertices()[end], visit, get_incoming)
            result += len(visit)
            torus.reset()
        probs.append(result/100.0)

    print("result: {0}".format(np.average(probs)))


def uniform_with_permanent_array(size,  permanent_part=0.25):
    threshold = 1.0 - permanent_part
    ans = EnvBuilder.np.random.random_sample(size)
    for i in xrange(size):
        if ans[i] < threshold:
            ans[i] = np.random.random()
        else:
            ans[i] = 1.0

    return ans


import time
def test_stochastic_algorithm(buildings_number, learning_number, torus_x=10, torus_y=10):
    start = 0
    finish = (torus_x/2)*torus_y + torus_y/2

    all_paths = []
    all_secondary = []
    RL_all_path = []
    times = np.zeros(buildings_number * learning_number, dtype=float)
    for i in xrange(buildings_number):
        torus = EnvBuilder.torus(torus_x, torus_y, uniform_with_permanent_array)
        v_finish = torus.get_vertex(finish)

        print("##"*25)
        print("outer loop #{0}".format(i))
        print("##"*25)

        for j in xrange(learning_number):
            print("inner loop #{0}".format(j))
            torus.reset()

            t1 = time.time()
            path_len, secondary_size = stoch_learning(v_finish.coords(), torus)
            RL_path_len = SARSA_test(v_finish.coords(), torus, 0.1, 0.9, 0.5) #
            t2 = time.time() - t1
            times[i * learning_number + j] = t2
            print("trial time in seconds: {0}".format(t2))

            all_paths.append(path_len)
            RL_all_path.append(RL_path_len)
            all_secondary.append(secondary_size)

        # save learning results from i_th generated graph
        #save_json_data("10x10_RL_vs_FS/all_paths_{0}.json".format(i + 1), all_paths[len(all_paths) -learning_number:])
        #save_json_data("10x10_RL_vs_FS/all_secondary_{0}.json".format(i + 1), all_secondary[len(all_secondary) -learning_number:])
        #save_json_data("10x10_RL_vs_FS/RL_all_path_{0}.json".format(i + 1), RL_all_path[-1: -learning_number-1:-1])
        print("##"*25)
        print("save data from learning on graph #{0}".format(i))
        print("##"*25)

    print("average trial time in seconds: {0}".format(np.average(times)))

    #all_paths = np.array(all_paths)
    #RL_all_path = np.array(RL_all_path)
    #all_secondary = np.array(all_secondary)

    #save_json_data("saturation5x5/mean_path.json", np.average([len(p) for p in all_paths]))

    #average_path = np.average(all_paths, axis=0)
    #average_RL_path = np.average(RL_all_paths, axis=0)
    #average_secondary = np.average(all_secondary, axis=0)

    #show_trials_with_median(all_paths, show=True, filename="10x10torus250/median_path")
    #show_trials_with_average(all_paths)
    #show_curves(range(0, len(average_path)), (last_n_averages(average_path, 50), "-", "Stochastic FS"))
    #show_trials_with_median(all_secondary, show=True, filename="10x10torus250/median_sec")


import os
import json
def ensure_dir(filename):
    """Check if directories in filename exists if not creates corresponding directories!"""
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)


def save_json_data(filename, data, rewrite=True):
    """Saves data in json format"""
    mode = "w" if rewrite else "a"

    ensure_dir(filename)
    with open(filename, mode) as the_file:
        json.dump(data, the_file)


def get_json_data(filename):
    """Reads data from json file"""
    data = None
    with open(filename, "r") as the_file:
        data = json.load(the_file)

    return data


def lists_average(lists):
    average = []
    y_max = max([len(l) for l in lists])
    for j in xrange(y_max):
        j_sum = 0.
        for i in xrange(len(lists)):
            j_sum += lists[i][j] if len(lists[i]) > j else lists[i][-1]
        average.append(j_sum / float(len(lists)))

    return average


import matplotlib.pyplot as plt
def show_trials_with_average(trials):
    np_trials = np.array(trials)

    x_axis = range(1, len(trials[0]) + 1)
    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111)

    for trial in trials:
        ax1.plot(x_axis, last_n_averages(trial, 20), color='gray')
        #ax1.plot(x_axis, trial, color='gray')

    average = np.average(np.array(trials), axis=0)
    ax1.plot(x_axis, average, color='black', lw=3.0)

    ax1.set_xlabel('trial')
    ax1.set_ylabel('path length')

    plt.show()


def show_trials_with_median(trials, show=True, filename=None):
    x_axis = range(1, len(trials[0]) + 1)
    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111)

    for trial in trials:
        ax1.plot(x_axis, trial, color='gray')

    median = calc_trials_median(trials)
    ax1.plot(x_axis, median, color='black', lw=3.0)

    ax1.set_xlabel('trial')
    ax1.set_ylabel('path length')
    #ax1.set_ylim(0, 200)

    if filename is not None:
        plt.savefig(filename)

    if show:
        plt.show()

    plt.clf()


def calc_trials_median(trials):
    if not isinstance(trials, np.ndarray):
        np_trails = np.array(trials)
    else:
        np_trails = trials

    y_len = np.shape(np_trails)[1]
    x_len = np.shape(np_trails)[0]

    sorted = np.sort(np_trails, axis=0)

    if x_len % 2 :
        get_median = lambda i: sorted[x_len/2][i]
    else:
        get_median = lambda i: (sorted[x_len/2][i] + sorted[x_len/2 - 1][i]) / 2.0

    median = [get_median(i) for i in xrange(y_len)]
    return median


def graph_path_len_to_net_size(path, net, show=True, filename=None):
    x_points = []
    y_points = []
    for i in xrange(len(path)):
        x_points.append(np.average(path[i]))
        y_points.append(net[i][-1])

    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111)

    ax1.plot(x_points, y_points,  'ob')

    ax1.set_xlabel('first trials average')
    ax1.set_ylabel('net size')
    ax1.set_ylim(0, 250)
    ax1.set_xlim(0, 250)

    if show:
        plt.show()

    if filename is not None:
        plt.savefig(filename)

    plt.clf()


def change_list2d_to_square(lists):
    y_len = max(len(l) for l in lists)
    for i in xrange(len(lists)):
        l_aver = np.average(lists[i][-1:-51:-1])
        for j in xrange(len(lists[i]), y_len):
            lists[i].append(l_aver)

    return lists


def path_len_correlation(paths1, paths2, name1="FS", name2="RL", show=True, filename=None):
    x_points = []
    y_points = []
    for i in xrange(len(paths1)):
        x_points.append(np.average(paths1[i][-10:]))  # average of last 10 trials
        y_points.append(np.average(paths2[i][-10:]))  # average of last 10 trials

    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111)

    ax1.plot(x_points, y_points,  'ob')

    maxx = max(max(x_points), max(y_points))
    ax1.set_xlabel(name1)
    ax1.set_ylabel(name2)
    ax1.set_ylim(0, maxx + 10)
    ax1.set_xlim(0, maxx + 10)

    if show:
        plt.show()

    if filename is not None:
        plt.savefig(filename)

    plt.clf()


if __name__ == "__main__":
    #create_complex_trial_sample()
    #ac.direct_action_tests()

    #net = single_learning((1, 1, 1), EnvBuilder.rhomb())
    #stoch_learning((1,1,1), EnvBuilder.rhomb())
    #dot.secondary_graph2dot(net)
    #env = EnvBuilder.stochastic_env2(0.7) #binary_choice(0.7) #stochastic_env2() #rhomb()
    #env.write_to_file("2dim_binary_choice.dot")

    test_stochastic_algorithm(10, 10, 10, 10)
    exit()

    """
    data_path = []
    data_net = []

    for i in xrange(1, 11):
        data_path.append(get_json_data("RL_vs_FS/all_paths_{0}.json".format(i))[5])
        data_net.extend(get_json_data("RL_vs_FS/all_secondary_{0}.json".format(i)))
    print np.shape(np.array(data_path))

    mean_path = np.mean(data_path, axis=0)
    wa_path = weighted_average(mean_path, 0.02)
    lastn_path = last_n_averages(mean_path, 50)
    show_curves(range(len(mean_path)), (mean_path, '-', "average beetween trials"))
    show_curves(range(len(mean_path)), (lastn_path, '-', "last 50 average"),
                (wa_path, '-', "weighted average alpha = 0.02"))

    std = lambda l, n: [np.std(l[max(0, i - n): i]) for i in range(1, len(l) + 1)]

    show_curves(range(len(mean_path)), (std(wa_path, 50), '-', "wa_50"),
                (std(lastn_path, 50), '-', "lastn_50"))
                #(std(wa_path, 10), '-', "wa_10"),
                #(std(lastn_path, 10), '-', "lastn_50"))
    #show_trials_with_average(median_fs)
    #show_trials_with_average(median_rl)

    #show_curves(range(0, len(aver_fs)), (aver_fs, "-", "FS"), (aver_rl, "-", "RL"))

    #data_path = change_list2d_to_square(data_path)
    #show_trials_with_median(data_path)
    #show_trials_with_average(data_path)
    #for i in xrange(0, 100, 10):
    #    show_trials_with_median(data[i:i+10],show=False, filename="test5x5/medians/path_median_{0}".format(i/10 + 1))
    #average = lists_average(data)
    #show_curves(range(0, len(average)), (average, "-", "average secondary net size"))
    exit()

    torus_x = 5
    torus_y = 5
    start = 0
    finish = (torus_x/2)*torus_y + torus_y/2
    torus = EnvBuilder.torus(torus_x, torus_y, uniform_with_permanent_array)
    v_finish = torus.get_vertex(finish)


    path_len, secondary_size = stoch_learning(v_finish.coords(), torus)

    with open('saturation_path.txt', 'w') as the_file:
        json.dump(path_len, the_file)

    with open('saturation_secondary.txt', 'w') as the_file:
        json.dump(secondary_size, the_file)

    print("Iteration number to complete learning = {0}".format(len(path_len)))
    show_curves(range(0, len(path_len)), (weighted_average(path_len, 0.025), "-", "awerage path length"))
    show_curves(range(0, len(secondary_size)), (secondary_size, "-", "secondary net size"))
        #torus.reset()
    exit()


    env = EnvBuilder.binary_choice(0.70) #stochastic_env2() #rhomb()

    bl = base_learning((1, 1, 1, 1, 1), env)
    sl = stoch_learning((1, 1, 1, 1, 1), env)
    #tl = tdl.td_learning((1, 1, 1, 1, 1), env, 0.01, 0.5, 1.0)
    sarsal1 = SARSA_test((1, 1, 1, 1, 1), env, 0.1, 0.9)
    sarsal2 = SARSA_test((1, 1, 1, 1, 1), env, 0.1, 0.9, 0.5)
    #sarsal4 = SARSA_test((1, 1, 1, 1, 1), env, 0.01, 0.1)
    ql1 = Q_learning_test((1, 1, 1, 1, 1), env, 0.1, 0.5, 0.5)
    ql2 = Q_learning_test((1, 1, 1, 1, 1), env, 0.1, 0.5, 0.9)
    ql3 = Q_learning_test((1, 1, 1, 1, 1), env, 0.1, 0.9, 0.9)

    #ql2 = Q_learning_test((1, 1, 1, 1, 1), env, 0.1, 0.1, 0.9)


    show_curves(range(0, len(sarsal1)),
        (weighted_average(sarsal1, 0.1), "-", "SARSA(alpha=0.9, gamma = 1.0)"),  # (weighted_average(bl, 0.03),"-", " base wa 0.01"),
        (weighted_average(sarsal2, 0.1), "-", "SARSA(alpha=0.9, gamma= 0.5)"),
        (weighted_average(ql1, 0.1), "-", "QL(alpha=0.5, gamma=0.5)"),
        (weighted_average(ql2, 0.1), "-", "QL(alpha=0.9, gamma=0.9)"),
        (weighted_average(ql3, 0.1), "-", "QL(alpha=0.9, gamma=0.9)"),
        (weighted_average(sl, 0.1), "-", "StochasticFS"))
        #(weighted_average(sarsal5, 0.02), "-", "SARSA(epsilon = 0.01, alpha=0.5)"),
        #(weighted_average(sarsal6, 0.02), "-", "SARSA(epsilon = 0.01, alpha=0.9)"))
       #(weighted_average(tl, 0.02), "-", "td weighted average a=0.02"))  # (weighted_average(sl, 0.03),"-", "stochastic wa 0.01"))

    #env.write_to_file("5dim_binary_choice.dot")
    #EnvBuilder.grid33()
    #net, vf, av = sln.new_single_learning((1, 1, 1, 1, 1), env)

    #dot.state_value_function2dot(net,vf, "secs_with_vf.dot")
    #dot.secondary_graph2dot(net, vf, "sec_decay.dot")
    #dot.environment2dot(env, vf, "env_valued.dot")

    #vf = sln.ValueFunction()
    #env1 = EnvBuilder.binary_choice()
    #dot.environment2dot(env1, vf)
    #env2 = EnvBuilder.stochastic_env1()
    #dot.environment2dot(env2, vf)

      t1 = np.random.randint(1,11, 2000) > 7
    t2 = np.random.randint(1,11, 2000) > 3
    t = list(t1)
    t.extend(t2)
    l = []
    v = 0.0
    alpha = 0.01
    for i in xrange(0, len(t)):
        v += alpha*(t[i] - v)
        l.append(v)

    show_curves(range(0, len(t)), (l, "-", "weighted average"))  # """
