# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        pass

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/zxing-cpp/zxing-cpp.git"
        self.defaultTarget = "2.3.0"
        self.targets[self.defaultTarget] = f"https://github.com/zxing-cpp/zxing-cpp/archive/v{self.defaultTarget}.tar.gz"
        self.archiveNames[self.defaultTarget] = f"zxing-cpp-v{self.defaultTarget}.tar.gz"
        self.targetInstSrc[self.defaultTarget] = f"zxing-cpp-{self.defaultTarget}"
        self.targetDigests[self.defaultTarget] = (["64e4139103fdbc57752698ee15b5f0b0f7af9a0331ecbdc492047e0772c417ba"], CraftHash.HashAlgorithm.SHA256)


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if CraftCore.compiler.isWindows:
            # There are some relative symbolic links causing "ERROR: Dangerous symbolic link path was ignored"
            self.subinfo.options.unpack.sevenZipExtraArgs = ["-snld"]

        self.subinfo.options.configure.args += ["-DBUILD_DEPENDENCIES=LOCAL", "-DBUILD_EXAMPLES=OFF", "-DBUILD_UNIT_TESTS=OFF", "-DBUILD_BLACKBOX_TESTS=OFF"]
