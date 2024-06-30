# -*- coding: utf-8 -*-
import os

import info
import utils
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.5.27","2.5.31"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/project/gphoto/libgphoto/{ver}/libgphoto2-{ver}.tar.bz2"
            self.archiveNames[ver] = f"libgphoto2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libgphoto2-{ver}"
        self.description = "Gphoto2 digital camera library"
        self.defaultTarget = "2.5.31"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libusb-compat"] = None
        self.runtimeDependencies["dev-utils/libtool"] = None
        # gd and libexif might be needed too
        if CraftCore.compiler.isMacOS:
            self.buildDependencies["libs/gettext"] = None


class Package(AutoToolsPackageBase):
    def fixLibraryFolder(self, folder):
        craftLibDir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib")
        for library in utils.filterDirectoryContent(str(folder)):
            for path in utils.getLibraryDeps(str(library)):
                if path.startswith(craftLibDir):
                    utils.system(["install_name_tool", "-change", path, os.path.join("@rpath", os.path.basename(path)), library])
            if library.endswith(".dylib"):
                utils.system(["install_name_tool", "-id", os.path.join("@rpath", os.path.basename(library)), library])
            utils.system(["install_name_tool", "-add_rpath", craftLibDir, library])

    def __init__(self, **args):
        super().__init__()
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.cflags += " -Wno-implicit-function-declaration"
        self.subinfo.options.configure.args += ["--disable-dependency-tracking", "--disable-silent-rules", f"--prefix={prefix}"]

    def install(self):
        ret = super().install()
        if CraftCore.compiler.isMacOS:
            self.fixLibraryFolder(self.imageDir() / "lib")
            self.fixLibraryFolder(self.imageDir() / "lib/libgphoto2/2.5.27")
            self.fixLibraryFolder(self.imageDir() / "lib/libgphoto2_port/0.12.0")
        return ret
