# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libsecret"] = None
        self.buildDependencies["libs/qt/qttools"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None

        # See https://github.com/frankosterfeld/qtkeychain/issues/262
        self.patchToApply["0.15.0"] = [("qtkeychain-0.15.0-20250201.diff", 1)]

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/frankosterfeld/qtkeychain.git"
        for ver in ["0.14.2", "0.14.3", "0.15.0", "0.17.0"]:
            self.targets[ver] = f"https://github.com/frankosterfeld/qtkeychain/archive/{ver}.tar.gz"
            self.archiveNames[ver] = f"qtkeychain-{ver}.tar.gz"
            self.targetInstSrc[ver] = "qtkeychain-%s" % ver
        self.targetDigests["0.14.2"] = (["cf2e972b783ba66334a79a30f6b3a1ea794a1dc574d6c3bebae5ffd2f0399571"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.14.3"] = (["a22c708f351431d8736a0ac5c562414f2b7bb919a6292cbca1ff7ac0849cb0a7"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.15.0"] = (["f4254dc8f0933b06d90672d683eab08ef770acd8336e44dfa030ce041dc2ca22"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.17.0"] = (["3b85c3929034b0a99da777130c34d99f006fcd3a9d56564159399a33fee0e504"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.17.0"
        self.releaseManagerId = 381807


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = ["-DBUILD_WITH_QT6=ON"]
