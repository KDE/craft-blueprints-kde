import info


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            # Theoretically gpgmepp supports mingw but the cmake patches are incomplete
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["1.21.0"] = [("cmake.patch", 1), ("gpgmepp-1.21.0-20231109.diff", 1)]
        self.patchLevel["1.21.0"] = 7

    def setDependencies(self):
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnupg"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.dynamic.buildStatic = False
        self.subinfo.options.configure.args += ["-DWITH_QT=ON"]

        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.subinfo.options.configure.args += ["-DQGPGME_BUILD_QT5=OFF"]
        else:
            self.subinfo.options.configure.args += ["-DQGPGME_BUILD_QT6=OFF"]
