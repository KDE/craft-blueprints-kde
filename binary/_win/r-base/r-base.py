# -*- coding: utf-8 -*-

import info

PACKAGE_CRAN_MIRROR = "https://ftp.gwdg.de/pub/misc/cran"
PACKAGE_PATH = "/bin/windows/base/old/"


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = None

    def setTargets(self):
        for version in ["4.2.0", "4.1.2", "3.6.2"]:
            self.targets[version] = PACKAGE_CRAN_MIRROR + PACKAGE_PATH + version + "/" + "R-" + version + "-win.exe"
        self.targets["devel"] = PACKAGE_CRAN_MIRROR + PACKAGE_PATH + "R-devel.exe"
        self.defaultTarget = "4.2.0"


from Package.BinaryPackageBase import *


# Installation approach based on expat-src-2.0.1.py.
# This basically just runs the upstream binary installer, then moves files to the KDE dir.
# Installation goes to dstdir/lib/R, since R comes with *a lot* of files in several subdirectories.
# This approach is also taken in the Debian packages, and probably other *n*x distributions.
# A convenience R.bat is added to dstdir/bin to have "R" in the path.
# Compiling R from source is possible, but terribly complex on Windows. See
# http://cran.r-project.org/doc/manuals/R-admin.html#Installing-R-under-Windows for details.
class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
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
        f = open(os.path.join(dstdir, "bin", "R.bat"), "w")
        f.write(
            "REM redirect to R.exe, autocreated during installation\n"
            + os.path.join("%~dsp0", "..", "lib", "R", "bin", "R.exe")
            + " %1 %2 %3 %4 %5 %6 %7 %8 %9\n"
        )
        f.close()

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
