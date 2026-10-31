# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.3.0"]:
            self.svnTargets[ver] = ""
        self.description = "The Cython compiler for writing C extensions in the Python language."
        self.defaultTarget = "3.3.0"
        self.releaseManagerId = 36699

    def setDependencies(self):
        self.buildDependencies["python-modules/setuptools"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
