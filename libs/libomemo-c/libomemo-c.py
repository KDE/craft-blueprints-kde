# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setDependencies(self):
        pass

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/dino/libomemo-c|omemo'
        self.defaultTarget = 'master'

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += ["-DBUILD_TESTING=OFF"]
