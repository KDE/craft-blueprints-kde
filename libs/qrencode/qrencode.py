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

    def setTargets(self):
        for ver in ["4.0.0"]:
            self.targets[ver] = f"https://fukuchi.org/works/qrencode/qrencode-{ver}.tar.gz"
            self.targetDigestUrls[ver] = ([f"https://fukuchi.org/works/qrencode/qrencode-{ver}.tar.gz.sha"], CraftHash.HashAlgorithm.SHA512)
            self.targetInstSrc[ver] = f"qrencode-{ver}"
        self.patchToApply["4.0.0"] = ("qrencode-4.0.0-20171220.diff", 1)

        self.description = "Libqrencode is a fast and compact library for encoding data in a QR Code symbol, a 2D symbology that can be scanned by handy terminals such as a mobile phone with CCD. The capacity of QR Code is up to 7000 digits or 4000 characters and has high robustness."
        self.defaultTarget = "4.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DWITH_TOOLS=OFF"]

    def install(self):
        if not super().install():
            return False
        # remove API docs here as there is no build option for that
        baseDir = os.path.join(self.installDir(), os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()))
        shutil.rmtree(os.path.join(baseDir, "man"), ignore_errors=True)
        return True
