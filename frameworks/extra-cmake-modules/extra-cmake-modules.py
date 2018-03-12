import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-utils/png2ico"] = "default"
        # needed for many kf5's
        self.buildDependencies["dev-utils/winflexbison"] = "default"
        self.buildDependencies["libs/qt5/qttools"] = "default"

        if CraftCore.settings.getboolean("CMake", "KDE_L10N_AUTO_TRANSLATIONS", False):
            self.buildDependencies["dev-utils/ruby"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
