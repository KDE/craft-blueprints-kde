import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/rkward'
        self.defaultTarget = 'master'
        self.displayName = "RKWard"

    def setDependencies(self):
        self.buildDependencies["extragear/rkward/rkward-translations"] = None
        self.runtimeDependencies["binary/r-base"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdewebkit"] = None
        # not strictly runtimeDependencies, but should be included in the package
        self.runtimeDependencies["kde/applications/kate"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.translations = CraftPackageObject.get("extragear/rkward/rkward-translations").instance

        if OsUtils.isWin():
            if CraftCore.compiler.isX64():
                self.r_dir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "bin", "x64")
            else:
                self.r_dir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "bin", "i386")
            self.subinfo.options.configure.args = " -DR_EXECUTABLE=" + OsUtils.toUnixPath(os.path.join(self.r_dir, "R.exe"))
        elif OsUtils.isMac():
            self.subinfo.options.configure.args = " -DR_EXECUTABLE=" + os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "R.framework", "Resources", "R")

        if self.subinfo.hasSvnTarget:
            self.subinfo.options.configure.args += f" -DTRANSLATION_SRC_DIR={OsUtils.toUnixPath(self.translations.sourceDir())}"

    def fetch(self):
        # Temporary workaround for failure to pull due to local modification of ver.R. Remove the line below around June, 2018.
        utils.deleteFile(os.path.join(self.checkoutDir(), "rkward", "rbackend", "rpackages", "rkward", "R", "ver.R"))

        if not CMakePackageBase.fetch(self):
            return False
        if self.subinfo.hasSvnTarget:
            return self.translations.fetch(noop=False)
        return True

    def install(self):
        ret = CMakePackageBase.install(self)
        if OsUtils.isWin():
            # Make installation movable, by providing rkward.ini with relative path to R
            rkward_ini = open(os.path.join(self.imageDir(), "bin", "rkward.ini"), "w")
            if CraftCore.compiler.isX64():
                rkward_ini.write("R executable=../lib/R/bin/x64/R.exe\n")
            else:
                rkward_ini.write("R executable=../lib/R/bin/i386/R.exe\n")
            rkward_ini.close()
        return ret

    def configure(self):
        if CraftCore.compiler.isMSVC():
            # Need to create a .lib-file for R.dll, first
            dump = subprocess.check_output(["dumpbin", "/exports", os.path.join(self.r_dir, "R.dll")]).decode(
                "latin1").splitlines()
            exports = []
            for line in dump:
                fields = line.split()
                if len(fields) != 4:
                    continue
                exports.append(fields[3])
            self.enterBuildDir()
            with open(os.path.join(self.buildDir(), "R.def"), "wt+") as deffile:
                deffile.write("EXPORTS\n")
                deffile.write("\n".join(exports))
            subprocess.call(["lib", "/def:R.def", "/out:R.lib", f"/machine:{CraftCore.compiler.architecture}"])
        return super().configure()

    def createPackage(self):
        self.defines["executable"] = "bin\\rkward.exe"
        self.defines["icon"] = os.path.join(self.sourceDir(), "rkward", "icons", "app-icon", "rkward.ico")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("data/hunspell-dictionaries")
        self.whitelist_file.append(os.path.join(self.packageDir(), 'whitelist.txt'))

        return TypePackager.createPackage(self)

    def preArchive(self):
        if OsUtils.isMac():
            # during packaging, the relative path between rkward and R gets changed, so we need to create an rkward.ini to help rkward find R
            rkward_dir = os.path.join(self.archiveDir(), "Applications", "KDE", "rkward.app", "Contents", "MacOS")
            utils.createDir(rkward_dir)
            rkward_ini = open(os.path.join(rkward_dir, "rkward.ini"), "w")
            rkward_ini.write("R executable=../Frameworks/R/R.framework/Resources/R\n")
            rkward_ini.close()
        return super().preArchive()
