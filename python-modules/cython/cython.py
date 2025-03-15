# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "The Cython compiler for writing C extensions in the Python language."
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["python-modules/setuptools"] = None

class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
