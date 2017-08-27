# -*-coding:utf-8-*-
from cnoid import Body, BodyPlugin
from util import IKParam
import numpy as np

# define function
## cnoid.Body.Body (robot)
def links(self):
    num=self.numLinks()
    return [self.link(link_i) for link_i in range(num)]

def jointList(self):
    num=self.numJoints()
    return [self.joint(joint_i) for joint_i in range(num)]

def angleVector(self,angles=None):
    if not angles is None:
        if self.numJoints() != len(angles):
            raise TypeError('length of angles do not agree with self.numJoints')
        for j,joint in enumerate(self.jointList()):
            joint.q=angles[j]
    return np.array([joint.q for joint in self.jointList()])

def set_ikparams(self, ee_names):
    self.ik_params = dict(zip([ee_name.lower().split("_")[0]
                               for ee_name in ee_names], # set eename (ex. RLEG_JOINT5 -> rleg)
                              [IKParam(self, ee_name)
                               for ee_name in ee_names])) # set ik param

def simple_ik(self):
    return [ik_param.manip.calcInverseKinematics(ik_param.p,
                                                 ik_param.R)
            for ik_param in self.ik_params.values()]

## cnoid.BodyPlugin.BodyItem (robotItem)
def drawBodyItem(self):
    self.calcForwardKinematics()
    self.notifyKinematicStateChange()
    return True

# add method
## cnoid.Body.Body (robot)
Body.Body.links=links
Body.Body.jointList=jointList
Body.Body.angleVector=angleVector
Body.Body.set_ikparams=set_ikparams
Body.Body.simple_ik=simple_ik

## cnoid.BodyPlugin.BodyItem (robotItem)
BodyPlugin.BodyItem.draw=drawBodyItem
