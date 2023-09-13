import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnupg"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.patchToApply["1.21.0"] = ("cmake.patch", 1)

        self.patchLevel["1.21.0"] = 2

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DWITH_QT=ON", "-DBUILD_SHARED_LIBS=ON"]


