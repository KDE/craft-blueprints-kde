import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://invent.kde.org/education/rkward.git'
        self.defaultTarget = 'master'
        self.displayName = "RKWard"

    def setDependencies(self):
        self.buildDependencies["extragear/rkward/rkward-translations"] = None
        self.runtimeDependencies["binary/r-base"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        if CraftCore.compiler.isMinGW():    # MinGW has not qtwebengine, but we can fall back to kdewebkit
            self.runtimeDependencies["kde/frameworks/tier3/kdewebkit"] = None
        else:
            self.runtimeDependencies['libs/qt5/qtwebengine'] = None
        # not strictly runtimeDependencies, but should be included in the package for plugins and extra functionality
        self.runtimeDependencies["kde/applications/kate"] = None
        if not OsUtils.isMac():
            # kbibtex does not properly build on mac, yet, and is optional
            self.runtimeDependencies["extragear/kbibtex"] = None
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
        elif OsUtils.isMac():
            # Fix absolute library locations for R libs. Users may use RKWard with various versions of R (installed, separately), so
            # we cannot set a stable relative path, either. However, the rkward frontend makes sure to cd to the appropriate directory
            # when starting the backend, so the libs can be found by basename.
            rkward_rbackend = os.path.join(self.imageDir(), "lib", "libexec", "rkward.rbackend")
            for path in utils.getLibraryDeps(str(rkward_rbackend)):
                if path.startswith("/Library/Frameworks/R.framework"):
                    utils.system(["install_name_tool", "-change", path, os.path.join("@rpath", os.path.basename(path)), rkward_rbackend])
            # Finally tell the loader to look in the current working directory (as set by the frontend)
            utils.system(["install_name_tool", "-add_rpath", ".", rkward_rbackend])
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

        if OsUtils.isMac():
            # We cannot reliably package R inside the bundle. Users will have to install it separately.
            self.ignoredPackages.append("binary/r-base")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("data/hunspell-dictionaries")
        self.whitelist_file.append(os.path.join(self.packageDir(), 'whitelist.txt'))
        # Certain plugin files defeat codesigning on mac, which is picky about file names
        if OsUtils.isMac():
            self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist_mac.txt'))

        return TypePackager.createPackage(self)

    def preArchive(self):
        if OsUtils.isMac():
            # On Mac there is no sane way to bundle R along with RKWard, so make the default behavior to detect an R installation, automatically.
            rkward_dir = os.path.join(self.archiveDir(), "Applications", "KDE", "rkward.app", "Contents", "MacOS")
            utils.createDir(rkward_dir)
            rkward_ini = open(os.path.join(rkward_dir, "rkward.ini"), "w")
            rkward_ini.write("R executable=auto\n")
            rkward_ini.close()
        return super().preArchive()
