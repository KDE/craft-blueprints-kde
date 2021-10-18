import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Plasma Wayland Protocols"
        self.description = "Plasma-specific protocols for Wayland"
        self.svnTargets["master"] = "https://invent.kde.org/libraries/plasma-wayland-protocols"

        for ver in ["1.3.0", "1.4.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/plasma-wayland-protocols/plasma-wayland-protocols-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"plasma-wayland-protocols-{ver}"

        self.targetDigests["1.3.0"] = (['0daa2362f2e0d15f79e0e006e8d7f1908e88e37b5c5208b40c9cb0d4d6dca9b5'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.4.0"] = (['38b0431d931a83393770abb8294206936b63b89ceee3f0c63f0f086f3d2b1ba9'], CraftHash.HashAlgorithm.SHA256)


        self.defaultTarget = "1.4.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
