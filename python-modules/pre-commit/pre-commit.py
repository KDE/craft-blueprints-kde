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
        self.buildDependencies["python-modules/hatchling"] = None
        self.buildDependencies["python-modules/virtualenv"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        return self.createMacOSPipShims(["pre-commit"])
