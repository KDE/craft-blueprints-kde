import os
import shutil

import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.7.5"]:
            self.targets[ver] = f"https://github.com/dmtx/libdmtx/archive/v{ver}.zip"
            self.archiveNames[ver] = f"libdmtx-{ver}.zip"
            self.targetInstSrc[ver] = f"libdmtx-{ver}"

        self.targetDigests["0.7.5"] = (["7c67be07bd5a952733bc47fa17cbb637e0ed8a2bbae78323b48961da0267a772"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["0.7.5"] = [("libdmtx-0.7.4-20180820.diff", 1)]

        self.description = "libdmtx is open source software for reading and writing Data Matrix barcodes on Linux, Unix, OS X, Windows, and mobile devices. At its core libdmtx is a native shared library, allowing C/C++ programs to use its capabilities without extra restrictions or overhead."
        self.defaultTarget = "0.7.5"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.bootstrap = True
        if self.subinfo.options.buildStatic:
            self.subinfo.options.configure.args += ["--enable-static=yes", "--enable-shared=no"]
        else:
            self.subinfo.options.configure.args += ["--enable-static=no", "--enable-shared=yes"]

    def install(self):
        if not super().install():
            return False
        # remove API docs here as there is no build option for that
        baseDir = os.path.join(self.installDir(), os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()))
        shutil.rmtree(os.path.join(baseDir, "man"), ignore_errors=True)
        return True
