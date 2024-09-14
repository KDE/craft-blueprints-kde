# -*- coding: utf-8 -*-

import os

import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase

PACKAGE_CRAN_MIRROR = "https://ftp.gwdg.de/pub/misc/cran"
PACKAGE_PATH = "/bin/windows/base/old/"


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        for version in ["4.3.3"]:
            self.targets[version] = PACKAGE_CRAN_MIRROR + PACKAGE_PATH + version + "/" + "R-" + version + "-win.exe"
        self.targets["devel"] = PACKAGE_CRAN_MIRROR + PACKAGE_PATH + "R-devel.exe"
        self.defaultTarget = "4.3.3"


# Installation approach based on expat-src-2.0.1.py.
# This basically just runs the upstream binary installer, then moves files to the KDE dir.
# Installation goes to dstdir/lib/R, since R comes with *a lot* of files in several subdirectories.
# This approach is also taken in the Debian packages, and probably other *n*x distributions.
# A convenience R.bat is added to dstdir/bin to have "R" in the path.
# Compiling R from source is possible, but terribly complex on Windows. See
# http://cran.r-project.org/doc/manuals/R-admin.html#Installing-R-under-Windows for details.
class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # don't use shortcut to unpack into imageDir()
        self.buildSystemType = "custom"
        # create combined package
        self.subinfo.options.package.withCompiler = None
        self.subinfo.options.unpack.runInstaller = True
        self.subinfo.options.configure.args = '/DIR="{0}" /SILENT /CURRENTUSER'.format(self.workDir())

    def install(self):
        srcdir = self.workDir()
        dstdir = self.installDir()
        r_rootdir = os.path.join(dstdir, "lib", "R")

        utils.cleanDirectory(dstdir)
        os.makedirs(r_rootdir)
        os.makedirs(os.path.join(dstdir, "bin"))

        # place everything in dstdir/lib/R (similar to debian packaging)
        CraftCore.installdb.getInstalledPackages(self.package)
        utils.copyDir(srcdir, r_rootdir)

        # create a shortcut in dstdir/bin
        utils.createShim(os.path.join(dstdir, "bin", "R.exe"), os.path.join(r_rootdir, "bin", "R.exe"))

        # Pre-install R2HTML-package. It will almost certainly be needed.
        utils.system(
            [
                os.path.join(r_rootdir, "bin", "R.exe"),
                "--no-save",
                "--slave",
                "--vanilla",
                "-e",
                "install.packages('R2HTML',lib=.Library[1],repos='https://ftp.gwdg.de/pub/misc/cran')",
            ]
        )

        return True
