import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Spelling framework for Qt, plugin-based."

    def registerOptions(self):
        self.options.dynamic.registerOption("useHunspell", True)


    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/hunspell"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        # always use just hunspell, if at all!
        self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_ASPELL=ON"
        if not self.subinfo.options.dynamic.useHunspell:
            self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_HUNSPELL=ON"
