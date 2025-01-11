# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None

    def setTargets(self):
        self.targets["2.7_1"] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/qtsoap-2.7_1-opensource.zip"
        self.patchToApply["2.7_1"] = ("qtsoap-2.7_1-opensource-20110308.diff", 1)
        self.targetDigests["2.7_1"] = "933ffd4215052af7eed48fc9492a1cd6996c7641"
        self.targetInstSrc["2.7_1"] = "qtsoap-2.7_1-opensource"
        self.defaultTarget = "2.7_1"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
