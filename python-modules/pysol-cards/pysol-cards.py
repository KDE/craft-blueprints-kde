# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.24.0"]:
            self.svnTargets[ver] = ""
        self.description = "Deal PySol FC Cards"
        self.defaultTarget = "0.24.0"
        self.releaseManagerId = 83432

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/setuptools"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
