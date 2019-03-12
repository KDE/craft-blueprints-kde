import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["18.08.1"] = [("libkexiv2-18.08.1-20180925.diff", 1)]

        self.patchLevel["18.12.1"] = 2
        for ver in self.targets:
            if CraftVersion(ver) % "18.12":
                self.patchToApply[ver] = [("libkexiv2-18.12.1-20190123.diff", 1)]

        self.description = "Libkexiv2 is a wrapper around Exiv2 library to manipulate pictures metadata as EXIF IPTC and XMP."

    def setDependencies(self):
        self.runtimeDependencies["libs/exiv2"] = None
        self.runtimeDependencies["kde/frameworks/extra-cmake-modules"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
