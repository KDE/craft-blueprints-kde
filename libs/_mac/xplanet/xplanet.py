# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3.1"]:
            self.targets[ver] = "https://downloads.sourceforge.net/project/xplanet/xplanet/" + ver + "/xplanet-" + ver + ".tar.gz"
            self.archiveNames[ver] = "xplanet-%s.tar.gz" % ver
        self.targetInstSrc["1.3.1"] = "xplanet-1.3.1"
        self.targetDigests["1.3.1"] = "e711dc5a561f83d5bafcc4e47094addfd1806af7"
        self.description = "xplanet, Create HQ wallpapers of planet Earth and time-updated images of other planets"
        self.defaultTarget = "1.3.1"
        self.patchToApply["1.3.1"] = ("xplanet-1.3.1-giflib5.patch", 1)
        self.patchToApply["1.3.1"] = ("xplanet-1.3.1-ntimes.patch", 1)

    def setDependencies(self):
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/giflib"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
        self.subinfo.options.configure.args = (
            "--disable-dependency-tracking"
            " --without-cspice"
            " --without-cygwin"
            " --without-gif"
            " --with-jpeg"
            " --without-libtiff"
            " --without-pango"
            " --without-pnm"
            " --without-x"
            " --without-xscreensaver"
            " --with-aqua"
            " --prefix=" + prefix
        )

        craftLibDir = os.path.join(prefix, "lib")

        self.subinfo.options.configure.ldflags = "-Wl -rpath " + craftLibDir + " -L" + craftLibDir

        # 	Note that this setting of the environment flags solves a build error on Sierra because the system headers have issues.

    def configure(self):
        prefix = self.shell.toNativePath(CraftCore.standardDirs.craftRoot())
        craftIncludeDir = os.path.join(prefix, "include")
        self.shell.environment["CXXFLAGS"] = "-I" + craftIncludeDir
        self.shell.environment["CFLAGS"] = "-I" + craftIncludeDir
        AutoToolsPackageBase.configure(self)
        return True
