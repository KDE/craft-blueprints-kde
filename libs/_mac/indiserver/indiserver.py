import glob
from xml.etree import ElementTree as et

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "INDI Library"
        self.svnTargets["master"] = "https://github.com/indilib/indi.git"
        self.targetInstSrc["master"] = ""

        ver = "v2.0.2"
        self.svnTargets["stable"] = "https://github.com/indilib/indi/archive/refs/tags/v%s.tar.gz" % ver
        self.archiveNames["stable"] = "indi-%s.tar.gz" % ver
        self.targetInstSrc["stable"] = ""

        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["dev-utils/grep"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/libnova"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/_mac/libusb"] = None
        self.runtimeDependencies["libs/_mac/theora"] = None
        self.runtimeDependencies["libs/libcurl"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/libev"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def fixLibraryFolder(self, folder):
        craftLibDir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib")
        for library in utils.filterDirectoryContent(str(folder)):
            for path in utils.getLibraryDeps(str(library)):
                if path.startswith(craftLibDir):
                    utils.system(["install_name_tool", "-change", path, os.path.join("@rpath", os.path.basename(path)), library])
            if library.endswith(".dylib"):
                utils.system(["install_name_tool", "-id", os.path.join("@rpath", os.path.basename(library)), library])
            utils.system(["install_name_tool", "-add_rpath", craftLibDir, library])

    def __init__(self):
        CMakePackageBase.__init__(self)
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root, "lib")
        self.subinfo.options.configure.args = (
            "-DCMAKE_INSTALL_PREFIX=" + root + " -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_MACOSX_RPATH=1 -DCMAKE_INSTALL_RPATH=" + craftLibDir
        )

    def install(self):
        ret = CMakePackageBase.install(self)
        if OsUtils.isMac():
            self.fixLibraryFolder(os.path.join(str(self.imageDir()), "lib"))
            self.fixLibraryFolder(os.path.join(str(self.imageDir()), "lib", "indi", "MathPlugins"))
            self.fixLibraryFolder(os.path.join(str(self.imageDir()), "bin"))
        return ret
