import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Linux

    def setTargets(self):
        self.displayName = "Plasma Wayland Protocols"
        self.description = "Plasma-specific protocols for Wayland"
        self.svnTargets["master"] = "https://invent.kde.org/libraries/plasma-wayland-protocols"

        for ver in ["1.10.0", "1.11.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/plasma-wayland-protocols/plasma-wayland-protocols-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/plasma-wayland-protocols/plasma-wayland-protocols-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"plasma-wayland-protocols-{ver}"

        self.patchToApply["1.11.0"] = [("fd5cda99a8c673f20de27ae73fbf244b5c8420d4.diff", 1)]
        self.patchLevel["1.11.0"] = 1

        self.defaultTarget = "1.11.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
