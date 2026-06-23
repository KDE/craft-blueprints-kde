# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.buildDependencies["libs/qt/qttools"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/gstreamer"] = None
        self.runtimeDependencies["libs/libomemo-c"] = None
        self.runtimeDependencies["libs/openssl"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/qxmpp.git"
        for ver in ["1.16.0"]:
            self.targets[ver] = f"https://download.kde.org/unstable/qxmpp/qxmpp-{ver}.tar.xz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"

        self.targetDigests["1.16.0"] = (["a421779635b2e2cb0b7b0aa34f7216ae53fd066160d008bbd32e580eae20c39c"], CraftHash.HashAlgorithm.SHA256)

        # https://invent.kde.org/libraries/qxmpp/-/merge_requests/778
        self.patchToApply["1.15.1"] = [("778.patch", 1)]

        self.defaultTarget = "1.16.0"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            "-DBUILD_EXAMPLES=OFF",
            f"-DBUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            "-DBUILD_OMEMO=ON",
            "-DWITH_GSTREAMER=ON",
        ]
