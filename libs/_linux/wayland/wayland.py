import os

import info
import utils
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.23.0"]:
            self.targets[ver] = f"https://gitlab.freedesktop.org/wayland/wayland/-/releases/{ver}/downloads/wayland-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"wayland-{ver}"
        self.targetDigestUrls["1.23.0"] = (
            ["https://gitlab.freedesktop.org/wayland/wayland/-/releases/1.23.0/downloads/wayland-1.23.0.tar.xz.sha256sum"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.description = "Core Wayland window system code and protocol"

        self.defaultTarget = "1.23.0"

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
