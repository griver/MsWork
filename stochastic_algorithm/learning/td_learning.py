# coding=utf-8
from fslib import Environment
import numpy as np
from . import stochastic_learning as sln


def epsilon_greedy_strategy(epsilon):
    """
    Возвращает функцию которая, принимая состояние среды и функцию ценности, делает epsilon-жадный выбор действия.
    """
    def epsilon_greedy_choice(vf, state):
        actions = state.get_outcoming()
        is_greedy = np.random.rand() >= epsilon

        if is_greedy:
            i = np.argmax(map(lambda x: vf.get(x), actions))
        else:
            i = np.random.randint(0, len(actions))

        return actions[i]

    return epsilon_greedy_choice


greedy_strategy = epsilon_greedy_strategy(0.0)


def SARSA(env, vf, goal, strategy, alpha, gamma, reward, penalty):
    assert isinstance(env, Environment)
    assert isinstance(vf, sln.ValueFunction)

    actions_number = 0
    action = strategy(vf, env.get_current_state())
    new_action = None

    while env.get_current_state() is not goal:
        if actions_number >= 2000: # for testing torus environment
            break
        index = env.get_current_state().get_outcoming().index(action)
        env.update_state(index)
        actions_number += 1
        next_vf = 0.0
        rw = 0.0

        if env.get_current_state() is goal:
            rw = reward
        else:
            if not action.is_available():
                rw = penalty
            new_action = strategy(vf, env.get_current_state())
            next_vf = vf.get(new_action)

        val = vf.get(action)
        val += alpha * (rw + gamma * next_vf - val)

        vf.put(action, val)
        action = new_action

    print("number of actions = " + str(actions_number))
    return actions_number


def Q_learning(env, vf, goal, strategy, alpha, gamma, reward, penalty):
    assert isinstance(env, Environment)
    assert isinstance(vf, sln.ValueFunction)

    actions_number = 0

    while env.get_current_state() is not goal:

        action = strategy(vf, env.get_current_state())
        index = env.get_current_state().get_outcoming().index(action)
        env.update_state(index)
        #env.update_state(action.get_dst().coords())
        actions_number += 1
        next_vf = 0.0
        rw = 0.0

        if env.get_current_state() is goal:
            rw = reward
        else:
            if not action.is_available():
                rw = penalty
            best_action = greedy_strategy(vf, env.get_current_state())
            next_vf = vf.get(best_action)

        val = vf.get(action)
        val += alpha * (rw + gamma * next_vf - val)

        vf.put(action, val)

    print("number of actions = " + str(actions_number))
    return actions_number


def td_learning(td_algorithm, goal_coordinates, env, trials_number=250, action_default=0.5):
    target = env.get_state_by_coords(goal_coordinates)
    env.reset()
    action_numbers = []
    i = 0

    vf = sln.ValueFunction()
    for v in env.vertices():
        vf.add_if_absent(v.get_outcoming(), action_default + np.random.rand() * 0.001)

    while True:
        print("----------------------------------------------------")
        i += 1
        an = td_algorithm(env, vf, target)
        action_numbers.append(an)

        if not i % trials_number:
            #if sln.ln.exit_condition():
            break

        env.reset()
        print("STEP:" + str(i))
        print("----------------------------------------------------")

    return action_numbers
