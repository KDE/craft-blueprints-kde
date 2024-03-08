import os

import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "INDI Library"
        self.svnTargets["master"] = "https://github.com/indilib/indi.git"
        self.targetInstSrc["master"] = ""

        ver = "v2.0.6"
        self.svnTargets["stable"] = f"https://github.com/indilib/indi/archive/refs/tags/v{ver}.tar.gz"
        self.archiveNames["stable"] = f"indi-{ver}.tar.gz"
        self.targetInstSrc["stable"] = ""

        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["dev-utils/grep"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/libnova"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/libusb"] = None
        self.runtimeDependencies["libs/theora"] = None
        self.runtimeDependencies["libs/libcurl"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/libev"] = None
        self.runtimeDependencies["libs/libxisf"] = None


class Package(CMakePackageBase):
    def fixLibraryFolder(self, folder):
        craftLibDir = CraftCore.standardDirs.craftRoot() / "lib"
        for library in utils.filterDirectoryContent(str(folder)):
            for path in utils.getLibraryDeps(str(library)):
                if path.startswith(craftLibDir):
                    utils.system(["install_name_tool", "-change", path, os.path.join("@rpath", os.path.basename(path)), library])
            if library.endswith(".dylib"):
                utils.system(["install_name_tool", "-id", os.path.join("@rpath", os.path.basename(library)), library])
            utils.system(["install_name_tool", "-add_rpath", craftLibDir, library])

    def __init__(self):
        super().__init__()
        root = CraftCore.standardDirs.craftRoot()
        craftLibDir = root / "lib"
        self.subinfo.options.configure.args += [
            f"-DCMAKE_INSTALL_PREFIX={root}",
            "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
            "-DCMAKE_MACOSX_RPATH=1",
            f"-DCMAKE_INSTALL_RPATH={craftLibDir}",
        ]

    def install(self):
        ret = super.install()
        if CraftCore.compiler.isMacOS:
            self.fixLibraryFolder(self.imageDir() / "lib")
            self.fixLibraryFolder(self.imageDir() / "lib/indi/MathPlugins")
            self.fixLibraryFolder(self.imageDir() / "bin")
        return ret
