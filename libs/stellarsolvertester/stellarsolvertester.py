import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Packager.AppxPackager import AppxPackager


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "StellarSolver Sextractor and Astrometry.net based Library Tester Program"
        self.svnTargets["master"] = "https://github.com/rlancaste/stellarsolver.git"
        for ver in ["2.7"]:
            self.targets[ver] = f"https://github.com/rlancaste/stellarsolver/archive/refs/tags/{ver}.tar.gz"
            self.archiveNames[ver] = f"stellarsolver-tester-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"stellarsolver-{ver}"
        self.defaultTarget = "2.7"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["libs/mman"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["boost-regex"] = None
        self.runtimeDependencies["libs/wcslib"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        craftLibDir = CraftCore.standardDirs.craftRoot() / "lib"
        self.subinfo.options.configure.args += [
            "-DCMAKE_MACOSX_RPATH=1",
            "-DBUILD_TESTER=ON",
            f"-DCMAKE_INSTALL_RPATH={craftLibDir}",
        ]

    def createPackage(self):
        self.defines["executable"] = "bin\\StellarSolverTester.exe"
        self.defines["icon"] = self.blueprintDir() / "StellarSolverInstallIcon.ico"
        if isinstance(self, AppxPackager):
            self.defines["display_name"] = "StellarSolverTester"
        return super().createPackage()
