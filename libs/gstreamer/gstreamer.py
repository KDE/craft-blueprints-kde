import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.20.0"]:
            self.targets[ver] = f"https://gitlab.freedesktop.org/gstreamer/gstreamer/-/archive/{ver}/gstreamer-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gstreamer-{ver}"
        self.targetDigests["1.20.0"] = (['1c97433269f008c7080ed9b6c2598933778921f522da1db144229b282bdc6b94'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.20.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/python3"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["python-modules/meson"] = None
        self.buildDependencies["dev-utils/bison"] = None
        self.buildDependencies["libs/libintl-lite"] = None

from Package.MesonPackageBase import *

class Package(MesonPackageBase):
    def __init__(self):
        MesonPackageBase.__init__(self)
