import os
import shutil

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.16.0']:
            self.targets[ver] = 'https://www.cairographics.org/releases/cairo-' + ver + '.tar.xz'
            self.targetInstSrc[ver] = 'cairo-' + ver
        self.targetDigests['1.16.0'] = (['5e7b29b3f113ef870d1e3ecf8adf21f923396401604bda16d44be45e66052331'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Multi-platform 2D graphics library"
        self.defaultTarget = '1.16.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/fontconfig"] = None
        self.runtimeDependencies["libs/pixman"] = None

from Package.AutoToolsPackageBase import *
from Package.MakeFilePackageBase import *

if CraftCore.compiler.isMSVC():
    class Package(MakeFilePackageBase):
        def __init__(self):
            MakeFilePackageBase.__init__(self)

        def includesFromPkgConfig(self, libName):
            includes = subprocess.run('pkg-config --cflags-only-I ' + libName, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip()
            includes = includes.replace(CraftCore.standardDirs.craftRoot().as_posix(), self._shell.toNativePath(CraftCore.standardDirs.craftRoot()))
            return includes

        def libsFromPkgConfig(self, libName):
            libs = subprocess.run('pkg-config --libs-only-l ' + libName, stdout=subprocess.PIPE, universal_newlines=True).stdout.strip()
            libs = libs.replace('-l', '')
            res = []
            for lib in libs.split():
                res.append(self._shell.toNativePath(CraftCore.standardDirs.craftRoot()) + "/lib/" + lib + ".lib")
            return ' '.join(res)

        def make(self):
            self._shell = BashShell()

            # Fix the path to our includes/libs
            win32common = self.sourceDir() / "build/Makefile.win32.common"
            with open(win32common, "rt") as f:
                content = f.read()

            # pixman include path
            content = content.replace("PIXMAN_CFLAGS := -I$(PIXMAN_PATH)/pixman/", "PIXMAN_CFLAGS := " + self.includesFromPkgConfig("pixman-1"))
            # pixman lib path
            content = content.replace("PIXMAN_LIBS := $(PIXMAN_PATH)/pixman/$(CFG)/pixman-1.lib", "PIXMAN_LIBS := " + self.libsFromPkgConfig("pixman-1"))
            # png lib path
            content = content.replace("CAIRO_LIBS +=  $(LIBPNG_PATH)/libpng.lib", "CAIRO_LIBS += " + self.libsFromPkgConfig("libpng"))
            # zlib lib path
            content = content.replace("CAIRO_LIBS += $(ZLIB_PATH)/zdll.lib", "CAIRO_LIBS += " + self.libsFromPkgConfig("zlib"))
            # freetype include path
            content = content.replace("DEFAULT_CFLAGS += $(PIXMAN_CFLAGS) $(LIBPNG_CFLAGS) $(ZLIB_CFLAGS)", "DEFAULT_CFLAGS += $(PIXMAN_CFLAGS) $(LIBPNG_CFLAGS) $(ZLIB_CFLAGS) " + self.includesFromPkgConfig("freetype2"))
            # freetype lib path
            # TODO fix freetype package so we can use self.libsFromPkgConfig here
            content = content.replace("CAIRO_LIBS =  gdi32.lib msimg32.lib user32.lib", "CAIRO_LIBS =  gdi32.lib msimg32.lib user32.lib " + self.libsFromPkgConfig("freetype2"))

            with open(win32common, "wt") as f:
                f.write(content)

            # Enable Freetype
            win32features = self.sourceDir() / "build/Makefile.win32.features"
            with open(win32features, "rt") as f:
                content = f.read()

            content = content.replace("CAIRO_HAS_FT_FONT=0", "CAIRO_HAS_FT_FONT=1")

            with open(win32features, "wt") as f:
                f.write(content)


            return self._shell.execute(self.sourceDir(), "make", ["-f", "Makefile.win32", "CFG=release"])

        def install(self):
            if not BuildSystemBase.install(self):
                return False

            for d in ["include", "bin", "lib"]:
                os.makedirs(self.installDir() / d, exist_ok=True)

            shutil.copyfile(self.sourceDir() / "cairo-version.h", self.installDir() / 'include/cairo-version.h')
            for f in ["cairo-features.h", "cairo.h", "cairo-deprecated.h", "cairo-win32.h", "cairo-script.h", "cairo-ps.h", "cairo-pdf.h", "cairo-svg.h", "cairo-ft.h"]:
                shutil.copyfile(self.sourceDir() / "src" / f, self.installDir() / 'include' / f)
            shutil.copyfile(self.sourceDir() / "src/release/cairo.dll", self.installDir() / 'bin/cairo.dll')
            shutil.copyfile(self.sourceDir() / "src/release/cairo.lib", self.installDir() / 'lib/cairo.lib')


            return True

else:
    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.autoreconf = False
            if CraftCore.compiler.isMinGW():
                self.subinfo.options.configure.cflags += " -fstack-protector"
