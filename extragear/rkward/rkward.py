import info
from CraftOS.osutils import OsUtils
from Packager.AppImagePackager import AppImagePackager


class subinfo(info.infoclass):
    def addReleaseCandidate(self, version, suffix):
        self.targets[f"{version}-{suffix}"] = f"https://files.kde.org/rkward/testing/for_packaging/rkward-{version}-{suffix}.tar.gz"
        self.targetInstSrc[f"{version}-{suffix}"] = f"rkward-{version}"

    def setTargets(self):
        self.description = "RKWard is an easy to use and easily extensible IDE/GUI for R."
        self.displayName = "RKWard"
        self.webpage = "https://rkward.kde.org"

        self.svnTargets["master"] = "https://invent.kde.org/education/rkward.git"
        self.addReleaseCandidate("0.7.5", "rc1")
        for ver in ["0.7.4"]:
            self.targets[ver] = f"https://download.kde.org/stable/rkward/{ver}/rkward-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"rkward-{ver}"
        self.targetDigests["0.7.4"] = (["7633f3b269f6cf2c067b3b09cbe3da3e0ffdcd9dc3ecb9a9fa63b4f865e8161e"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.7.5-rc1"

    def setDependencies(self):
        if OsUtils.isWin() or OsUtils.isMac():
            self.runtimeDependencies["binary/r-base"] = None
        else:
            self.runtimeDependencies["libs/r-base"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["libs/qt5/qtscript"] = None
        if CraftCore.compiler.isMinGW() or OsUtils.isMac() and CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            # MinGW has no qtwebengine, but we can fall back to kdewebkit
            self.runtimeDependencies["kde/frameworks/tier3/kdewebkit"] = None
        else:
            self.runtimeDependencies["libs/qt/qtwebengine"] = None
        # not strictly runtimeDependencies, but should be included in the package for plugins and extra functionality
        self.runtimeDependencies["kde/applications/kate"] = None
        if not OsUtils.isMac():
            # kbibtex does not properly build on mac, yet, and is optional
            self.runtimeDependencies["extragear/kbibtex"] = None
        # optional, but should be in the package
        self.runtimeDependencies["binary/pandoc"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        if OsUtils.isWin():
            # For packaging with Innosetup-packager, which is not the default packager (yet)
            self.buildDependencies["dev-utils/innosetup"] = None
        if OsUtils.isLinux():
            # NOTE: the following are not actually direct dependencies, but rather an optional dependency of kate->kuserfeedback, and others
            #       Added, here, as a workaround, because kuserfeedback may have been built with the lib in the cache, without anything declaring the dependency
            self.runtimeDependencies["libs/qt/qtcharts"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
            self.runtimeDependencies["libs/qt5/qtserialport"] = None
            # Needed at runtime to keep libcurl working inside the AppImage. See definition of CURL_CA_BUNDLE, below.
            self.runtimeDependencies["core/cacert"] = None
            # Needed for building some R packages
            self.runtimeDependencies["dev-utils/sed"] = None
            # tags io-slave used by KEncodingFileDialog (producing ugly warning, if not present)
            self.runtimeDependencies["kde/frameworks/tier3/baloo"] = None
        elif OsUtils.isMac():
            # indirectly required by kate, but not declared as dependency, there
            self.runtimeDependencies["kde/frameworks/tier2/kactivities"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        if OsUtils.isWin():
            # Usually found, automatically, but make extra sure, never to pick up a separate installation of R
            r_dir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "bin", "x64")
            self.subinfo.options.configure.args += [f"-DR_EXECUTABLE={OsUtils.toUnixPath(os.path.join(r_dir, 'R.exe'))}"]
        elif OsUtils.isMac():
            rhome = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "R.framework", "Resources")
            self.subinfo.options.configure.args += [
                f"-DR_EXECUTABLE={os.path.join(rhome, 'R')}",
                "-DNO_CHECK_R=1",
                f"-DR_HOME={rhome}",
                f"-DR_INCLUDEDIR={os.path.join(rhome, 'include')}",
                f"-DR_SHAREDLIBDIR={os.path.join(rhome, 'lib')}",
                "-DUSE_BINARY_PACKAGES=1",
                "-DNO_QT_WEBENGINE=1",
            ]

    def fetch(self):
        if not CMakePackageBase.fetch(self):
            return False
        return True

    def setDefaults(self, defines: {str: str}) -> {str: str}:
        defines = super().setDefaults(defines)
        if OsUtils.isLinux() and isinstance(self, AppImagePackager):
            defines["runenv"].append('CURL_CA_BUNDLE="$this_dir/etc/cacert.pem"')
            defines["runenv"].append('LD_LIBRARY_PATH="$this_dir/usr/lib:$LD_LIBRARY_PATH"')  # R misses custom loaded libbzip2.so without this
        return defines

    def install(self):
        ret = CMakePackageBase.install(self)
        if OsUtils.isWin() or OsUtils.isLinux():
            # Make installation movable, by providing rkward.ini with relative path to R
            rkward_ini = open(os.path.join(self.imageDir(), "bin", "rkward.ini"), "w")
            if OsUtils.isLinux():
                rkward_ini.write("R executable=../lib/R/bin/R\n")
            else:
                rkward_ini.write("R executable=../lib/R/bin/x64/R.exe\n")
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
        if OsUtils.isWin() and (not CraftCore.settings.get("Packager", "PackageType", "")):
            self.changePackager("InnoSetupPackager")

        self.defines["executable"] = "bin\\rkward.exe"
        self.defines["icon"] = os.path.join(self.sourceDir(), "rkward", "icons", "app-icon", "rkward.ico")
        self.defines["file_types"] = [".R", ".Rdata", ".Rmd", ".rko"]

        if OsUtils.isMac():
            # We cannot reliably package R inside the bundle. Users will have to install it separately.
            self.ignoredPackages.append("binary/r-base")
            self.externalLibs = {"@rpath/libR.dylib", "@rpath/libRblas.dylib", "@rpath/libRlapack.dylib"}

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("data/hunspell-dictionaries")
        self.whitelist_file.append(os.path.join(self.packageDir(), "whitelist.txt"))
        # Certain plugin files defeat codesigning on mac, which is picky about file names
        if OsUtils.isMac():
            self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist_mac.txt"))

        return TypePackager.createPackage(self)

    def reinplace(self, filename, old, new):
        CraftCore.log.info(f"patching {old} -> {new} in {filename}")
        with open(filename, "r") as f:
            content = f.read()
        with open(filename, "w") as f:
            f.write(content.replace(old, new))

    def preArchive(self):
        if OsUtils.isMac():
            # On Mac there is no sane way to bundle R along with RKWard, so make the default behavior to detect an R installation, automatically.
            rkward_dir = os.path.join(self.archiveDir(), "Applications", "KDE", "rkward.app", "Contents", "MacOS")
            utils.createDir(rkward_dir)
            rkward_ini = open(os.path.join(rkward_dir, "rkward.ini"), "w")
            rkward_ini.write("R executable=auto\n")
            rkward_ini.close()
        if OsUtils.isLinux() and isinstance(self, AppImagePackager):
            for filename in ["bin/R", "lib/R/bin/R", "lib/R/bin/libtool", "lib/R/etc/ldpaths", "lib/R/etc/Renviron"]:
                filename = os.path.join(self.archiveDir(), filename)
                self.reinplace(filename, str(CraftCore.standardDirs.craftRoot()), "${APPDIR}/usr")
            for filename in ["lib/R/etc/Makeconf"]:
                filename = os.path.join(self.archiveDir(), filename)
                self.reinplace(filename, str(CraftCore.standardDirs.craftRoot()), "$(APPDIR)/usr")  # NOTE: round braces, here
            # quirkaround for making kioslaves work despite of https://github.com/linuxdeploy/linuxdeploy/issues/208 / https://invent.kde.org/packaging/craft/-/merge_requests/80
            for subpath in ["libexec/lib", "lib/libexec/lib", "plugins/lib", "plugins/kf5/lib"]:
                utils.createSymlink(os.path.join(self.archiveDir(), "lib"), os.path.join(self.archiveDir(), subpath), targetIsDirectory=True)
        return super().preArchive()
