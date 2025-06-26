# -*- coding: utf-8 -*-
import os

import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "xplanet, Create HQ wallpapers of planet Earth and time-updated images of other planets"

        for ver in ["1.3.1"]:
            self.targets[ver] = f"https://downloads.sourceforge.net/project/xplanet/xplanet/{ver}/xplanet-{ver}.tar.gz"
            self.archiveNames[ver] = f"xplanet-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"xplanet-{ver}"

        self.targetDigests["1.3.1"] = "e711dc5a561f83d5bafcc4e47094addfd1806af7"
        self.patchToApply["1.3.1"] = [
            ("xplanet-1.3.1-aqua.patch", 1),
            ("xplanet-1.3.1-giflib5.patch", 1),
            ("xplanet-1.3.1-ntimes.patch", 1),
            ("xplanet-c++11.patch", 1)]

        self.defaultTarget = "1.3.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/giflib"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "--disable-dependency-tracking",
            "--disable-asm-optimizations",
            "--without-cspice",
            "--without-cygwin",
            "--without-gif",
            "--with-jpeg",
            "--without-libtiff",
            "--without-pango",
            "--without-pnm",
            "--without-x",
            "--without-xscreensaver",
            "--with-aqua",
        ]

        craftLibDir = self.shell.toNativePath(CraftCore.standardDirs.craftRoot() / "lib")

        self.subinfo.options.configure.ldflags = f"-Wl -rpath {craftLibDir} -L{craftLibDir}"

        # 	Note that this setting of the environment flags solves a build error on Sierra because the system headers have issues.

    def configure(self):
        prefix = self.shell.toNativePath(CraftCore.standardDirs.craftRoot())
        craftIncludeDir = os.path.join(prefix, "include")
        self.shell.environment["CXXFLAGS"] += f"-I{craftIncludeDir} -Wno-c++11-narrowing"
        self.shell.environment["CFLAGS"] += f"-I{craftIncludeDir}"
        super().configure()
        return True
