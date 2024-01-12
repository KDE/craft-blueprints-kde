# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    # def setDependencies( self ):

    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "Python 2 and 3 compatibility utilities"
        self.defaultTarget = "master"


class Package(PipPackageBase):
    def __init__(self, **args):
        super().__init__()
