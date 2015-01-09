__author__ = 'griver'

from fslib import FunctionalSystem
from fslib import BaseSecondary


class LMSecondary(BaseSecondary):
    def __init__(self, net, env, motivation, prev_st, goal_st, calc_IA, calc_AR, calc_ii, delta_si):
        BaseSecondary.__init__(self,
                               "Sec(" + str(motivation.get_id()) + "): " + str(prev_st.get_id()) + " -> " + str(goal_st.get_id()),
                               active_threshold=0.96)
        self._delta_si = delta_si
        self._newS = 0
        self._newIA = 0
        self._newAR = 0
        self._newI = 0

        self._env = env
        self._net = net
        self._motiv_fs = motivation
        self._prev_state = prev_st
        self._goal_state = goal_st

        self._delta_si = delta_si
        self._calc_IA = calc_IA
        self._calc_AR = calc_AR
        self._calc_ii = calc_ii

        self._active_time = 0

    def recalculate_params(self):  # calculate new parameters of fs
        self._newIA = self._calc_IA(self)
        self._newAR = self._calc_AR(self)
        self._newI = self._calc_ii(self)
        self._newS = self._S + self._delta_si(self)
        self.deactivation_method()

    def apply_new_params(self):  # self-describing name
        self._S = self._newS
        self._IA = self._newIA
        self._AR = self._newAR
        self._I = self._newI

    def get_motivation(self):
        return self._motiv_fs

    def get_net(self):
        return self._net

    def get_cnet(self):
        return self._net.get_cnet(self._cnet_name)

    def deactivation_method(self):
        if self.is_active(): self._active_time += 1
        else: self._active_time = 0

        #if self._active_time == 201 and not self._deactivated:
        #    print(self.name + " is not deactivated!")

        if self._active_time == 20 or self._deactivated:
            self._deactivated = True
            self._newR = 0
            self._newS = 0


class OneActivationSecondary(LMSecondary):
    def deactivation_method(self):
        if self.is_active(): self._active_time += 1
        else: self._active_time = 0

        if (self._active_time > 0 and self._newI == 0.0) or self._active_time == 20:
            self._deactivated = True
