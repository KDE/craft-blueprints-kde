# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    # def setDependencies( self ):

    def setTargets(self):
        self.svnTargets["master"] = ""
        self.defaultTarget = "master"


class Package(PipPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.python2 = False

    def install(self):
        pythonPath = CraftCore.settings.get("Paths", "PYTHON")
        utils.createShim(os.path.join(self.imageDir(), "bin", "pylint.exe"), os.path.join(pythonPath, "scripts", "pylint"), useAbsolutePath=True)
        return PipBuildSystem.install(self)
