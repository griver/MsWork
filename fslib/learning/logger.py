from fslib import BaseFSNetwork
from fslib import Environment


class TrialLogger(object):

    def __init__(self):
        self._states = [] # mapping form time to environment state
        self._fs_activities = []
        self._path = []
        self._actions = []
        self._count = 0
        self._last_start = None
        self._last_count = 0

    def add(self, net, env):
        #assert isinstance(net, BaseFSNetwork)
        #assert isinstance(env, Environment)
        self._count += 1
        self._states.append(env.get_current_state().get_id())


        if self._path[-1] != env.get_current_state():
            self._path.append(env.get_current_state())
            self._actions.append(net.get_last_action())

        for i in xrange(len(self._fs_activities), len(net.vertices())):
            self._fs_activities.append([])

        for i in xrange(0, len(net.vertices())):
            self._fs_activities[i].append(net.get_vertex(i).get_S())

    def get_states(self):
        return self._states

    def get_fs_activities(self):
        return self._fs_activities

    def get_path(self):
        return self._path

    def get_actions(self):
        return self._actions

    def get_count(self):
        return self._count

    def get_last_count(self):
        return self._last_count

    def get_last_start(self):
        return self._last_start

    def start_trial(self, env, net):
        if len(self._path) == 0:
            self._path.append(env.get_current_state())

        self._last_start = len(self._path) - 1
        self._last_count = self._count


    def reset(self):
        self.clear()


    def clear(self):
        self._count = 0
        self._states = []
        self._fs_activities = []
        self._path = []
        self._actions = []