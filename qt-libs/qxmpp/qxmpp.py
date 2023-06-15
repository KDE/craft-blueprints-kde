# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


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
        for ver in ["1.5.4"]:
            self.targets[ver] = f"https://github.com/qxmpp-project/qxmpp/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"qxmpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qxmpp-{ver}"
        self.targetDigests["1.5.4"] = (["e437fdb91aa52c6fd8ca3f922354eb3221df98146ec99ee92e70e20a82c7ad2d"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.5.4"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args = "-DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF -DBUILD_OMEMO=ON"
