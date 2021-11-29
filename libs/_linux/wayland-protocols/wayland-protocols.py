import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.24"]:
            self.targets[ver] = f"https://wayland.freedesktop.org/releases/wayland-protocols-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"wayland-protocols-{ver}"
        self.targetDigests['1.24'] = (['bff0d8cffeeceb35159d6f4aa6bab18c807b80642c9d50f66cba52ecf7338bc2'], CraftHash.HashAlgorithm.SHA256)

        self.description = "wayland-protocols contains Wayland protocols that add functionality not available in the Wayland core protocol."

        self.defaultTarget = "1.24"


from Package.MesonPackageBase import *

class Package(MesonPackageBase):
    def __init__(self):
        MesonPackageBase.__init__(self)

