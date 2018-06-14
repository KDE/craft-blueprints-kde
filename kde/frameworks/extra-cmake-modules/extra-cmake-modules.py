import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.versionInfo.tarballs() + self.versionInfo.branches() + self.versionInfo.tags():
            ecmVer = CraftVersion(ver)
            if ecmVer <= CraftVersion("5.47.0"):
              self.patchLevel[ver] = 2
              self.patchToApply[ver] = ('icotool.diff', 1)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-utils/icoutils"] = "default"
        # needed for many kf5's
        self.buildDependencies["dev-utils/flexbison"] = "default"
        self.buildDependencies["libs/qt5/qttools"] = "default"

        if CraftCore.settings.getboolean("CMake", "KDE_L10N_AUTO_TRANSLATIONS", False):
            self.buildDependencies["dev-utils/ruby"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
