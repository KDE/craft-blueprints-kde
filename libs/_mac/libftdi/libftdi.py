# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4"]:
            self.targets[ver] = "https://www.intra2net.com/en/developer/libftdi/download/libftdi1-%s.tar.bz2" % ver
            self.archiveNames[ver] = "libftdi1-%s.tar.bz2" % ver
            self.targetInstSrc[ver] = "libftdi1-" + ver
        self.description = "Library to talk to FTDI chips"
        self.defaultTarget = "1.4"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["libs/swig"] = None
        self.buildDependencies["libs/_mac/libusb"] = None
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        root = str(CraftCore.standardDirs.craftRoot())
        self.subinfo.options.configure.args = "-DPYTHON_BINDINGS=OFF -DEXAMPLES=OFF -DBUILD_TESTS=OFF"
        # self.subinfo.options.configure.cflags = f"-I{root}/include"
        # self.subinfo.options.configure.cxxflags = f"-I{root}/include"

    def postQmerge(self):
        packageName = "libftdi1"
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root, "lib")
        utils.system("install_name_tool -add_rpath " + craftLibDir + " " + craftLibDir + "/" + packageName + ".dylib")
        utils.system("install_name_tool -id @rpath/" + packageName + ".dylib " + craftLibDir + "/" + packageName + ".dylib")
        return True
