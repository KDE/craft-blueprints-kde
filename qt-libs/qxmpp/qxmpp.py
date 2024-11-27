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
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.buildDependencies["libs/qt6/qt5compat"] = None
        self.runtimeDependencies["libs/libomemo-c"] = None
        self.runtimeDependencies["kdesupport/qca"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/qxmpp-project/qxmpp.git"
        for ver in ["1.9.0", "1.9.1"]:
            self.targets[ver] = f"https://github.com/qxmpp-project/qxmpp/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"
        self.targetDigests["1.9.0"] = (["1b791c53d32e38c7f612b4a1d54f35b9db264501be2b3d07ef927af73e2f7d0e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.9.1"] = (["940b9510ce21ec1daac2047fc2fbbe899d17c868dd872af03c6c8f9b3490b4d6"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.9.1"


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()

        self.subinfo.options.configure.args += ["-DBUILD_EXAMPLES=OFF", "-DBUILD_TESTS=OFF", "-DBUILD_OMEMO=ON"]
