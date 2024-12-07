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
        for ver in ["1.9.0", "1.9.2"]:
            self.targets[ver] = f"https://github.com/qxmpp-project/qxmpp/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"
        self.targetDigests["1.9.0"] = (["1b791c53d32e38c7f612b4a1d54f35b9db264501be2b3d07ef927af73e2f7d0e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.9.2"] = (["b6ddfe446ce5f628d3bc3a2a8d09ea86cdb9b7773435d112192e416f5a69981d"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.9.2"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += ["-DBUILD_EXAMPLES=OFF", "-DBUILD_TESTS=OFF", "-DBUILD_OMEMO=ON"]
