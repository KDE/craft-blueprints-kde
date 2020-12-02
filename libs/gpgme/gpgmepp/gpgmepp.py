import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.targetDigests['1.11.1'] = (['2d1b111774d2e3dd26dcd7c251819ce4ef774ec5e566251eb9308fa7542fbd6f'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.14.0"] = (['cef1f710a6b0d28f5b44242713ad373702d1466dcbe512eb4e754d7f35cd4307'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['1.11.1'] = ("gpgme-1.11.1-20201101.diff", 1)
        self.patchToApply['1.14.0'] = [ ("gpgme-1.14.0-20201106.diff", 1),
                                        ("gpgmepp-1.14.0-20201106.diff", 1),
                                        ("gpgmepp-1.14.0-20201113.diff", 1),
                                        ("gpgmepp-1.14.0-20201116.diff", 1),
                                        ("gpgmepp-1.14.0-20201117.diff", 1)]
        self.patchLevel["1.14.0"] = 3
        if CraftCore.compiler.isWindows:
            self.targets["skip-windows"] = ""
            self.defaultTarget = "skip-windows"

    def setDependencies(self):
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnupg"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += "-DWITH_CPP=ON -DWITH_QT=ON -DBUILD_SHARED_LIBS=ON"
        if self.buildTarget == "skip-windows":
            def warn():
                CraftCore.log.warning("Skipping build on windows, *everything is broken*, if you are adventurous try:\n\t'craft --set version=cmake libs/gpgme'")
                return True
            self.compile = warn
            self.install = lambda : utils.createDir(self.imageDir())
            self.createPackage = warn


