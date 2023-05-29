# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None

    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/KDAB/KDReports.git"
        for ver in ["2.0.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDReports/archive/kdreports-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"KDReports-kdreports-{ver}"
            self.archiveNames[ver] = f"kdreports-{ver}.tar.gz"
        self.targetDigests["2.0.0"] = (["59c215a424d5520690eaf27dbe8b02f1aeebd9fac822890692ff42de5d1e50f6"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.0.0"

        self.description = "Qt library for generating printable and exportable reports from code and from XML descriptions."
        self.webpage = "http://www.kdab.com/kd-reports/"
        self.displayName = "KDReports"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
