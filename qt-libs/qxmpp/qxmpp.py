# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.buildDependencies["libs/qt/qttools"] = None
        self.buildDependencies["libs/qt6/qt5compat"] = None
        self.runtimeDependencies["libs/gstreamer"] = None
        self.runtimeDependencies["libs/libomemo-c"] = None
        self.runtimeDependencies["kdesupport/qca"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/qxmpp.git"
        for ver in ["1.14.5"]:
            self.targets[ver] = f"https://download.kde.org/unstable/qxmpp/qxmpp-{ver}.tar.xz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"
        self.targetDigests["1.14.5"] = (["fcf809743cf9bf10884d700ad7d47e4d3e7063bdda30f6341d96f88e93809576"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.14.5"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            "-DBUILD_EXAMPLES=OFF",
            f"-DBUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            "-DBUILD_OMEMO=ON",
            "-DWITH_GSTREAMER=ON",
        ]
