# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["6.0.3"]:
            self.svnTargets[ver] = ""
        self.description = "PyYAML is a Python module that implements the next generation YAML parser and emitter."
        self.defaultTarget = "6.0.3"
        self.releaseManagerId = 48867

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/setuptools"] = None
        self.buildDependencies["python-modules/cython"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
