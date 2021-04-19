# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.buildDependencies["python-modules/libxml2-python3"] = None

class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
