import math as m
from fslib import Environment
from fslib.fs.lmimpl.lm_secondary import LMSecondary
from fslib import BaseSecondary
import random
import numpy as np

MIN_IA = 0.98

def sec_IA_maker(ia_value = MIN_IA):

    def calc_ia(fs):
        assert isinstance(fs, LMSecondary)
        assert isinstance(fs._env, Environment)
        env = fs._env
        edge = next((e for e in fs.get_incoming() if e.get_src() == fs._motiv_fs), None)
        if fs.IA_point() == env.get_current_state() and fs._motiv_fs.is_active():
            return ia_value + 0.0002 * random.random()
        else:
            return 0.0

    return calc_ia

def sec_AR_maker(ia_value = MIN_IA):

    def calc_ar(fs):
        return 0

    return calc_ar

def sec_ii_maker( threshold):

    def calc_ii(fs):
        assert isinstance(fs, LMSecondary)

        l = lambda e: isinstance(e.get_src(),BaseSecondary) and e.get_src().IA_point() == fs.IA_point()
        inc = filter(l, fs.get_incoming())
        sum = 0
        n = 0
        for e in inc:
            s = e.get_src().get_S()
            if s > threshold:
                sum += s
                n += 1

        mean = sum
        return (n * fs.get_S() >= mean) * fs._newIA

    return calc_ii

def delta_si(fs):
    assert isinstance(fs, LMSecondary)
    return fs._newI/2.0 - fs.get_S()/2.0