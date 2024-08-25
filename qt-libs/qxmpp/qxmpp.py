# -*- coding: utf-8 -*-
import info
from Blueprints.CraftPackageObject import CraftPackageObject
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
        self.svnTargets["master"] = "https://github.com/qxmpp-project/qxmpp.git"
        for ver in ["1.7.1", "1.8.1"]:
            self.targets[ver] = f"https://github.com/qxmpp-project/qxmpp/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"
        self.targetDigests["1.7.1"] = (["2691e2b28dfc45c4cda17ce04cf998b8c15f01bbf72f335e01b98a2f98063ef0"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.8.1"] = (["f307dde71dbaf9e17dc0472fafe68cabe2572b22ae759b6af24f8e1183b8db71"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.8.1"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += ["-DBUILD_EXAMPLES=OFF", "-DBUILD_TESTS=OFF", "-DBUILD_OMEMO=ON"]
