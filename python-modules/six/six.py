# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.17.0"]:
            self.svnTargets[ver] = ""
        self.description = "Python 2 and 3 compatibility utilities"
        self.defaultTarget = "1.17.0"
        self.releaseManagerId = 4027

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.buildDependencies["python-modules/setuptools"] = None
        self.runtimeDependencies["libs/python"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
