import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Linux

    def setTargets(self):
        self.displayName = "Plasma Wayland Protocols"
        self.description = "Plasma-specific protocols for Wayland"
        self.svnTargets["master"] = "https://invent.kde.org/libraries/plasma-wayland-protocols"

        for ver in ["1.8.0", "1.9.0", "1.10.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/plasma-wayland-protocols/plasma-wayland-protocols-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/plasma-wayland-protocols/plasma-wayland-protocols-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"plasma-wayland-protocols-{ver}"

        self.defaultTarget = "1.10.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
