# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/rekonq'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies['kde/kdelibs'] = 'default'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
