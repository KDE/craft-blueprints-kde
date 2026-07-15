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
        for ver in ["0.14.1", "0.14.2", "0.14.3", "0.15.0", "0.16.0"]:
            self.targets[ver] = f"https://github.com/frankosterfeld/qtkeychain/archive/{ver}.tar.gz"
            self.archiveNames[ver] = f"qtkeychain-{ver}.tar.gz"
            self.targetInstSrc[ver] = "qtkeychain-%s" % ver
        self.targetDigests["0.14.1"] = (["afb2d120722141aca85f8144c4ef017bd74977ed45b80e5d9e9614015dadd60c"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.14.2"] = (["cf2e972b783ba66334a79a30f6b3a1ea794a1dc574d6c3bebae5ffd2f0399571"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.14.3"] = (["a22c708f351431d8736a0ac5c562414f2b7bb919a6292cbca1ff7ac0849cb0a7"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.15.0"] = (["f4254dc8f0933b06d90672d683eab08ef770acd8336e44dfa030ce041dc2ca22"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.16.0"] = (["3be26ec4ae30eecf0c2ff7572ba83799791b157c76e15a05ef35f23dc25e4054"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.16.0"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = ["-DBUILD_WITH_QT6=ON"]
