import os

import info
import utils
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.24.0"]:
            self.targets[ver] = f"https://invent.kde.org/mirrors/wayland/-/archive/{ver}/wayland-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"wayland-{ver}"
        self.targetDigests["1.24.0"] = (["ef9224f1a8b6dbd3049a2e51a547abb7e89612414c192a4349f3c83c7f553672"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Core Wayland window system code and protocol"

        self.defaultTarget = "1.24.0"

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-Ddocumentation=false"]

    def install(self):
        if not super().install():
            return False
        pkgConfigSrc = self.installDir() / os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()) / "pkgconfig"
        pkgConfigDest = self.installDir() / "lib/pkgconfig"
        if pkgConfigSrc.exists():
            return utils.createDir(pkgConfigDest.parent) and utils.moveFile(pkgConfigSrc, pkgConfigDest)
        return True
