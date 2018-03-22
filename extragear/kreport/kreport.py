import info
from CraftOS.osutils import OsUtils

class subinfo(info.infoclass):
    def setTargets(self):
        versions = ['3.1', 'master']
        for ver in versions:
            self.svnTargets[ver] = f"git://anongit.kde.org/kreport|{ver}"
        self.defaultTarget = versions[0]
        self.description = "A framework for the creation and generation of reports in multiple formats"
        self.options.configure.args = " -DBUILD_EXAMPLES=ON"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-utils/python2"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebkit"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = "default" # hard dependency for now
        self.runtimeDependencies["extragear/kproperty"] = "default"
        # TODO Windows/Mac: add marble libs (we only need marble widget), for now marble libs are disabled there
        if not OsUtils.isWin() and not OsUtils.isMac():
            self.runtimeDependencies["kde/applications/marble"] = "default"

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
