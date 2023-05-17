import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        # https://raw.githubusercontent.com/microsoft/vcpkg/a618637937298060bdbe5fbcfb628eabd1082c8a/ports/qtimageformats/no_target_promotion_latest.patch
        self.patchToApply["6.4.3"] = [("no_target_promotion_latest.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/webp"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
