import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4"]:
            self.targets[ver] = f"https://gitlab.freedesktop.org/vdpau/libvdpau/-/archive/{ver}/libvdpau-{ver}.tar.bz2"
            self.targetInstSrc[ver] = "libvdpau-" + ver
        self.targetDigests["1.4"] = (["4258824c5a4555ef31de0a7d82b3caf19e75a16a13949f1edafc5f6fb2d33f30"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Video Decode and Presentation API for Unix. Developed by NVIDIA for Unix/Linux systems."
        self.defaultTarget = "1.4"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)
