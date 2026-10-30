# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "A framework for managing and maintaining multi-language pre-commit hooks."
        self.webpage = "https://pre-commit.com/"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/setuptools"] = None
        self.runtimeDependencies["python-modules/cfgv"] = None
        self.runtimeDependencies["python-modules/identify"] = None
        self.runtimeDependencies["python-modules/nodeenv"] = None
        self.runtimeDependencies["python-modules/pyyaml"] = None
        self.runtimeDependencies["python-modules/virtualenv"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        return self.createMacOSPipShims(["pre-commit"])
