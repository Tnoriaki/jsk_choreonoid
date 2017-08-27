#!/usr/bin/env python

import os
import roslib
import time
from jsk_choreonoid import body_util
from jsk_choreonoid.util import load_model
from cnoid import BodyUtil
import numpy as np

def measure_time(func, *args, **kwargs):
    N = kwargs.get("N")
    if N is None:
        N = 10000
    start = time.time()
    for i in xrange(N):
        ret = func(*args)
    print str(time.time() - start) + " [s]"
    return ret

if __name__ == "__main__":
    model_path = os.path.join(roslib.packages.get_pkg_dir("hrp2_models"),
                              "HRP2JSKNT_for_OpenHRP3/HRP2JSKNTmain.wrl")
    robot, robotItem, worldItem = load_model(model_path) # use choreonoid
    # robot = load_model(model_path, use_choreonoid=False) # not use choreonoid

    for name, args in zip(["angleVector", "links", "jointList"],
                          [(np.random.randn(34),), (), ()]):
        print "--------------------------------------------------"
        print name
        ret = []
        for message, module in zip(["python", "use c++ & boost python"], [body_util, BodyUtil]):
            print message
            ret.append(measure_time(getattr(module, name), robot, *args, N=1000))
            robot.angleVector(np.zeros(34))
        if name == "angleVector":
            np.testing.assert_array_almost_equal(ret[0], ret[1])

        reset_pose = np.array([0.,  0., -0.45378561,  0.87266463, -0.41887902,  0.,  0.,  # RLEG 0-6
                               0.,  0., -0.45378561,  0.87266463, -0.41887902,  0.,  0.,  # LLEG 0-6
                               0.,  0.,  # CHEST 0-1
                               0.,  0.,  # HEAD 0-1
                               0.17453293, -0.17453293,  0., -0.43633231,  0.,  0., -0.17453293, 0.26179939,  # RLEG 0-7
                               0.17453293,  0.17453293,  0., -0.43633231,  0.,  0., -0.17453293, -0.26179939])  # LLEG 0-7
    robot.set_ikparams(["LLEG_JOINT5", "RLEG_JOINT5"])
