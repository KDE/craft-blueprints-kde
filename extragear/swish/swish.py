# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies['libs/boost/boost-system'] = None
        self.buildDependencies['libs/boost/boost-thread'] = None
        self.buildDependencies['libs/boost/boost-locale'] = None
        self.buildDependencies['libs/boost/boost-date-time'] = None
        self.buildDependencies["libs/washer"] = None
        self.buildDependencies["libs/wtl"] = None
        self.buildDependencies["dev-utils/comet"] = None



    def setTargets(self):
        version = 'master'
        self.defaultTarget = version
        self.svnTargets[version] = 'https://github.com/brute4s99/swish.git'
        self.description = "SFTP Plugin for Windows 10"
        self.displayName = "Swish"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
