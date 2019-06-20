# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/brute4s99/comet.git'
        self.targetInstallPath["master"] = "dev-utils"
        self.defaultTarget = 'master'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)