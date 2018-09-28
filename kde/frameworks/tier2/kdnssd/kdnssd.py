import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        # https://raw.githubusercontent.com/KDE-mac/homebrew-kde/master/Formula/kf5-kdnssd.rb
        self.patchToApply["5.50.0"] = [("fix-mac.diff", 1)]
        self.description = "KDNSSD Framework"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
