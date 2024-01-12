# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        """ """
        self.svnTargets["svnHEAD"] = "git://qt.code.qt.io/qt-labs/jom.git"
        self.svnTargets["mingw"] = "git://gitorious.org/~saroengels/qt-labs/jom-mingw.git"
        self.svnTargets["cmake"] = "git://gitorious.org/~saroengels/qt-labs/jom-cmake.git"
        self.svnTargets["static"] = "git://qt.code.qt.io/qt-labs/jom.git"
        self.svnTargets["static-cmake"] = "git://gitorious.org/~saroengels/qt-labs/jom-cmake.git"
        self.targetSrcSuffix["cmake"] = "cmake"
        self.targetSrcSuffix["mingw"] = "mingw"

        self.defaultTarget = "svnHEAD"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/qlalr"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        flexpath = os.path.join(CraftStandardDirs.craftRoot(), "msys", "bin", "flex.exe")
        self.subinfo.options.configure.args += [f"-DFLEX_EXECUTABLE={flexpath}", "-DJOM_ENABLE_TESTS=ON"]
        if self.buildTarget.startswith("static"):
            qmakepath = os.path.join(CraftStandardDirs.craftRoot(), "qt-static", "bin", "qmake.exe")
            self.subinfo.options.configure.args += [f"-DQT_QMAKE_EXECUTABLE={qmakepath}"]
