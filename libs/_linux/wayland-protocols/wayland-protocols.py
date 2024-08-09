import os

import info
import utils

from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.36"]:
            self.targets[ver] = f"https://gitlab.freedesktop.org/wayland/wayland-protocols/-/releases/{ver}/downloads/wayland-protocols-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"wayland-protocols-{ver}"
        self.targetDigests["1.36"] = (["71fd4de05e79f9a1ca559fac30c1f8365fa10346422f9fe795f74d77b9ef7e92"], CraftHash.HashAlgorithm.SHA256)

        self.description = "wayland-protocols contains Wayland protocols that add functionality not available in the Wayland core protocol."

        self.defaultTarget = "1.36"

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-Dtests=false"]

    def install(self):
        if not super().install():
            return False
        pkgConfigSrc = self.installDir() / os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot()) / "pkgconfig"
        pkgConfigDest = self.installDir() / "lib/pkgconfig"
        if pkgConfigSrc.exists():
            return utils.createDir(pkgConfigDest.parent) and utils.moveFile(pkgConfigSrc, pkgConfigDest)
        return True
