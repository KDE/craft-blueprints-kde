# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None

    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/KDAB/KDReports.git"
        for ver in ["1.7.1", "1.9.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDReports/archive/kdreports-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"KDReports-kdreports-{ver}"
            self.archiveNames[ver] = f"kdreports-{ver}.tar.gz"
        self.targetDigests["1.7.1"] = (
            ["d75f4bf3399bea51837b7a931be8640823168ba19d6dfd346db3e2270a26ca23"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.9.0"] = (
            ["7bf970e2836b14cfd143e60ede2d2a4fcc23904d23079adb0ae63ea5604c010e"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply['1.7.1'] = [("KDReports-kdreports-1.7.1-20171220.diff", 1),
                                      ("0001-unittests-CMakeLists.txt-don-t-call-qt_wrap_cpp-sinc.patch", 1)]

        self.defaultTarget = "1.9.0"

        self.description = "Qt library for generating printable and exportable reports from code and from XML descriptions."
        self.webpage = "http://www.kdab.com/kd-reports/"
        self.displayName = "KDReports"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
