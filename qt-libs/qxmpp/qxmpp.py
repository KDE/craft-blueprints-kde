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
        self.runtimeDependencies["libs/libomemo-c"] = None
        self.runtimeDependencies["kdesupport/qca"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/qxmpp.git"
        for ver in ["1.9.4", "1.10.1"]:
            self.targets[ver] = f"https://invent.kde.org/libraries/qxmpp/-/archive/v{ver}/qxmpp-v{ver}.tar.gz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"
        self.targetDigests["1.9.4"] = (["53ec8c6dbedb647290ae97b7f60de42e08986983de8bdedb2dcb3bd6d4793bf3"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.10.1"] = (["5b0368aa13681148b0d5b6fff9dc1a6a1d83f098e94b8224c9a7cf0981a74038"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.10.1"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            "-DBUILD_EXAMPLES=OFF",
            f"-DBUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            "-DBUILD_OMEMO=ON",
        ]
