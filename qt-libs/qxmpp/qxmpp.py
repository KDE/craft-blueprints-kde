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
        for ver in ["1.7.1", "1.8.2"]:
            self.targets[ver] = f"https://github.com/qxmpp-project/qxmpp/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"
        self.targetDigests["1.7.1"] = (["2691e2b28dfc45c4cda17ce04cf998b8c15f01bbf72f335e01b98a2f98063ef0"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.8.2"] = (["5964468778c743ae336ebc14af9fda1afcc1128acc94d9500f4276614e5a1425"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.8.2"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += ["-DBUILD_EXAMPLES=OFF", "-DBUILD_TESTS=OFF", "-DBUILD_OMEMO=ON"]
