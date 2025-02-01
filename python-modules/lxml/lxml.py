# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = ""
        self.description = "Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API."
        self.defaultTarget = "master"

        # TODO: Make it building on MSVC
        self.allowPrebuildBinaries = CraftCore.compiler.isMSVC()


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
