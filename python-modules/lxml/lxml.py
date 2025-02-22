# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API."
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["python-modules/setuptools"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["python-modules/cython"] = None

class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = False
