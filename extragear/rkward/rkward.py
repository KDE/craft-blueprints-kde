import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "RKWard is an easy to use and easily extensible IDE/GUI for R."
        self.displayName = "RKWard"
        self.webpage = "https://rkward.kde.org"

        self.svnTargets['master'] = 'https://invent.kde.org/education/rkward.git'
        for ver in ['0.7.2']:
            self.targets[ver] = f'https://download.kde.org/stable/rkward/{ver}/src/rkward-{ver}.tar.gz'
            self.targetInstSrc[ver] = f'rkward-{ver}'
        self.targetDigests["0.7.2"] = (['452350a4057d9dc87bb7c7e2f5c38b5cb9715b42141186b0e8c4a28e3dd2adf6'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '0.7.2'

    def setDependencies(self):
        self.runtimeDependencies["binary/r-base"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["libs/qt5/qtscript"] = None
        if CraftCore.compiler.isMinGW() or OsUtils.isMac():
            # MinGW has no qtwebengine, but we can fall back to kdewebkit
            self.runtimeDependencies["kde/frameworks/tier3/kdewebkit"] = None
        else:
            self.runtimeDependencies['libs/qt5/qtwebengine'] = None
        # not strictly runtimeDependencies, but should be included in the package for plugins and extra functionality
        self.runtimeDependencies["kde/applications/kate"] = None
        if not OsUtils.isMac():
            # kbibtex does not properly build on mac, yet, and is optional
            self.runtimeDependencies["extragear/kbibtex"] = None
        # optional, but should be in the package
        self.runtimeDependencies["binary/pandoc"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        if OsUtils.isWin():
            # Usually found, automatically, but make extra sure, never to pick up a separate installation of R
            if CraftCore.compiler.isX64():
                r_dir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "bin", "x64")
            else:
                r_dir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "bin", "i386")
            self.subinfo.options.configure.args += [f"-DR_EXECUTABLE={OsUtils.toUnixPath(os.path.join(r_dir, 'R.exe'))}"]
        elif OsUtils.isMac():
            rhome = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "R.framework", "Resources")
            self.subinfo.options.configure.args += " -DR_EXECUTABLE=" + os.path.join(rhome, "R") + " -DNO_CHECK_R=1 -DR_HOME=" + rhome + " -DR_INCLUDEDIR=" + os.path.join(rhome, "include") + " -DR_SHAREDLIBDIR=" + os.path.join(rhome, "lib")
            self.subinfo.options.configure.args += " -DUSE_BINARY_PACKAGES=1"
            self.subinfo.options.configure.args += " -DNO_QT_WEBENGINE=1"

    def fetch(self):
        if not CMakePackageBase.fetch(self):
            return False
        if self.subinfo.buildTarget == "master":
            utils.system([sys.executable, os.path.join(self.checkoutDir(), "scripts", "import_translations.py")])
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
            rlibs = ["libR.dylib", "libRblas.dylib", "libRlapack.dylib"]
            for path in utils.getLibraryDeps(str(rkward_rbackend)):
                if os.path.basename(path) in rlibs:
                    utils.system(["install_name_tool", "-change", path, os.path.join("@rpath", os.path.basename(path)), rkward_rbackend])
            # Finally tell the loader to look in the current working directory (as set by the frontend)
            utils.system(["install_name_tool", "-add_rpath", ".", rkward_rbackend])
        return ret

    def createPackage(self):
        self.defines["executable"] = "bin\\rkward.exe"
        self.defines["icon"] = os.path.join(self.sourceDir(), "rkward", "icons", "app-icon", "rkward.ico")

        if OsUtils.isMac():
            # We cannot reliably package R inside the bundle. Users will have to install it separately.
            self.ignoredPackages.append("binary/r-base")
            self.externalLibs = {"@rpath/libR.dylib", "@rpath/libRblas.dylib", "@rpath/libRlapack.dylib"}

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
