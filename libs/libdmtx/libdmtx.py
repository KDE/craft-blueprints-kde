import os
import shutil

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.platform.isAndroid:
            self.options.dynamic.setDefault("buildStatic", True)
        self.options.dynamic.setDefault("buildTests", False)

    def setTargets(self):
        for ver in ["0.7.8"]:
            self.targets[ver] = f"https://github.com/dmtx/libdmtx/archive/v{ver}.zip"
            self.archiveNames[ver] = f"libdmtx-{ver}.zip"
            self.targetInstSrc[ver] = f"libdmtx-{ver}"

        self.targetDigests["0.7.8"] = (["3e79cc187028623890ecaf366a4a2e0afc07941acbd3705c5f7149f972726737"], CraftHash.HashAlgorithm.SHA256)
        self.description = "libdmtx is open source software for reading and writing Data Matrix barcodes on Linux, Unix, OS X, Windows, and mobile devices. At its core libdmtx is a native shared library, allowing C/C++ programs to use its capabilities without extra restrictions or overhead."
        self.defaultTarget = "0.7.8"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.configure.args = [
            f"-DDEFAULT_STATIC_LIBS={self.subinfo.options.dynamic.buildStatic.asOnOff}",
            f"-DDEFAULT_SHARED_LIBS={self.subinfo.options.dynamic.buildStatic.inverted.asOnOff}",
        ]

    def install(self):
        if not super().install():
            return False
        # remove API docs here as there is no build option for that
        baseDir = os.path.join(self.installDir(), os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()))
        shutil.rmtree(os.path.join(baseDir, "man"), ignore_errors=True)
        return True
