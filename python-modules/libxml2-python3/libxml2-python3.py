# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'

    def setDependencies(self):
        # I had to install host libxml2-devel and python3-devel
        # pip failed to find craft's
        self.buildDependencies["libs/libxml2"] = None


class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
