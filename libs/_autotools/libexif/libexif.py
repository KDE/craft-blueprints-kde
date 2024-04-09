import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.6.23"]:
            self.targets[ver] = f"https://github.com/libexif/libexif/releases/download/v{ver}/libexif-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libexif-{ver}"
        self.description = "A library for parsing, editing, and saving EXIF data"
        self.defaultTarget = "0.6.23"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
