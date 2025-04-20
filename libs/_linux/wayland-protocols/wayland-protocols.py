import os

import info
import utils
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.36"]:
            self.targets[ver] = f"https://invent.kde.org/mirrors/wayland-protocols/-/archive/{ver}/wayland-protocols-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"wayland-protocols-{ver}"
        self.targetDigests["1.36"] = (["e6830b04c19f6aa76c7e9cc91d5dd442f6df6f7b1e43ac62f7b04daf95b01737"], CraftHash.HashAlgorithm.SHA256)

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
