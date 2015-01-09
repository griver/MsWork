# coding=utf-8
from fslib.learning.logger import TrialLogger
import fslib

class TrialActionInfo:
    """
    TrialActionInfo - структура для хранения информации о действии агента во время испытания.
    :motor - действие(соответствующая моторная фс)
    :new_state - новое состояние в которое перешел агент, если действие не удалось то None
    :sec - вторичная фс которая побудила агент к действию, если таковой не было то None
    """
    def __init__(self, motor = None, new_state = None, secondary = None):
        self.motor = motor
        self.sec = secondary
        self.new_state = new_state

        def __str__(self):
            str = "mot: " +  motor.name
            if self.sec != None:
                str += "|sec: " + self.sec.name
            if self.new_state != None:
                str += "|st: " + self.new_state


class CompetitiveNetworkError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class SecondaryLogger(TrialLogger):
    """
    Расширение TrialLogger. Для каждого действия агента(активация моторной фс) заполняет структуру TrialActionInfo.
    После испытания эта информация используется для обновления функции ценности
    """
    def __init__(self):
        TrialLogger.__init__(self)
        self.trial_history = []
        self._prev_action = None
        self._prev_state = None

    def add(self, net, env):
        TrialLogger.add(self,net, env)

        assert isinstance(net, fslib.BaseFSNetwork)
        action = net.get_action()
        if action != self._prev_action:
            self._prev_action = action
            if action is not None:
                sec = self._get_secondary(net, action)
                if self._prev_state == env.get_current_state():
                    info = TrialActionInfo(action, None, sec)
                else:
                    info = TrialActionInfo(action, env.get_current_state(), sec)
                    self._prev_state = env.get_current_state()
                self.trial_history.append(info)

    def start_trial(self, env, net):
        TrialLogger.start_trial(self, env, net)
        self.trial_history = []
        self._prev_action = None
        self._prev_state = env.get_current_state()

    #def reset(self):
    #    self.clear()

    def clear(self):
        TrialLogger.clear(self)
        self.trial_history = []
        self._prev_action = None
        self._prev_state = None

    def _get_secondary(self, net, motor):
        assert isinstance(motor, fslib.BaseMotor)
        secs = filter(lambda e: isinstance(e.get_src(), fslib.BaseSecondary) and e.get_src().is_active() ,motor.get_incoming())
        if len(secs) == 0:
            return None
        elif len(secs) > 1:
            raise CompetitiveNetworkError("Несколько вторичных фс, вероятно из одной конурентой сети, одновременно активны!")
        else:
            return secs[0].get_src()
