import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.92.0"] = [("sonnet-5.92.0-20220322.diff", 1)]

        if CraftCore.compiler.isMinGW():
            self.patchToApply["5.95.0"] = [("fix-mingw-prefix.diff", 1)]
            self.patchLevel["5.95.0"] = 1

        self.description = "Spelling framework for Qt, plugin-based."

    def registerOptions(self):
        # hunspell just when needed, on Windows(visual studio) or Mac we try with the OS specific checkers
        self.options.dynamic.registerOption("useHunspell", CraftCore.compiler.isLinux)

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

        if self.options.dynamic.useHunspell:
            self.runtimeDependencies["libs/hunspell"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        # always use just hunspell, if at all!
        self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_ASPELL=ON"
        if not self.subinfo.options.dynamic.useHunspell:
            self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_HUNSPELL=ON"
