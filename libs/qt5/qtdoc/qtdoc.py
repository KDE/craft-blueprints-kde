# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5"] = "default"

from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        self.subinfo.options.make.args = "docs"
        self.subinfo.options.install.args = "install_docs"


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
