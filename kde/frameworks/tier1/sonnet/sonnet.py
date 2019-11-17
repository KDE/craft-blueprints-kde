import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Spelling framework for Qt, plugin-based."

        self.patchToApply["5.64.0"] = [
            ("ispellchecker.patch", 1),
        ]

        self.patchLevel["5.64.0"] = 1

    def registerOptions(self):
        # hunspell just on unices, on Windows or Mac we try with the OS specific checkers
        if OsUtils.isUnix():
            self.options.dynamic.registerOption("useHunspell", True)

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

        # hunspell just on unices, on Windows or Mac we try with the OS specific checkers
        if OsUtils.isUnix():
            self.runtimeDependencies["libs/hunspell"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        # always use just hunspell, if at all!
        self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_ASPELL=ON"
        if not self.subinfo.options.dynamic.useHunspell:
            self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_HUNSPELL=ON"
