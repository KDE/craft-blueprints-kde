# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    # def setDependencies( self ):

    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "Python 3 compatible Python 2 'random' Module"
        self.defaultTarget = "master"


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
