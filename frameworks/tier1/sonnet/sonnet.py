import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.43.0"] = [("0001-Find-libhunspell-build-by-msvc.patch", 1),
                                       ("0002-Use-Locale-name-instead-of-Locale-bcp47Name.patch", 1)]
        self.patchLevel["5.43.0"] = 1

        self.description = "Spelling framework for Qt, plugin-based."

    def registerOptions(self):
        self.options.dynamic.registerOption("useHunspell", True)
        self.options.dynamic.registerOption("useAspell", False)


    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/hunspell"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if not self.subinfo.options.dynamic.useHunspell:
            self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_HUNSPELL=ON"
        if not self.subinfo.options.dynamic.useAspell:
            self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_ASPELL=ON"
