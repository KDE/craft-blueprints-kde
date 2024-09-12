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

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/frankosterfeld/qtkeychain.git"
        for ver in ["0.14.1", "0.14.2", "0.14.3"]:
            self.targets[ver] = f"https://github.com/frankosterfeld/qtkeychain/archive/{ver}.tar.gz"
            self.archiveNames[ver] = "qtkeychain-{ver}.tar.gz"
            self.targetInstSrc[ver] = "qtkeychain-%s" % ver
        self.targetDigests["0.14.1"] = (["afb2d120722141aca85f8144c4ef017bd74977ed45b80e5d9e9614015dadd60c"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.14.2"] = (["cf2e972b783ba66334a79a30f6b3a1ea794a1dc574d6c3bebae5ffd2f0399571"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.14.3"] = (["a22c708f351431d8736a0ac5c562414f2b7bb919a6292cbca1ff7ac0849cb0a7"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.14.3"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = ["-DBUILD_WITH_QT6=ON"]
