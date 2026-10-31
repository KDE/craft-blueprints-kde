# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/setuptools"] = None

    def setTargets(self):
        for ver in ["0.6.0"]:
            self.svnTargets[ver] = ""
        self.description = "Doxyqml is an input filter for Doxygen, a documentation system for C++ and a few other languages."
        self.defaultTarget = "0.6.0"
        self.releaseManagerId = 321160


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
