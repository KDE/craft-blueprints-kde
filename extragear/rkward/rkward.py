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
        # self.addReleaseCandidate("0.7.5", "rc1")
        # for ver in ["0.7.4"]:
        #    self.targets[ver] = f"https://download.kde.org/stable/rkward/{ver}/rkward-{ver}.tar.gz"
        #    self.targetInstSrc[ver] = f"rkward-{ver}"
        # self.targetDigests["0.7.4"] = (["7633f3b269f6cf2c067b3b09cbe3da3e0ffdcd9dc3ecb9a9fa63b4f865e8161e"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "master"

    def setDependencies(self):
        if OsUtils.isWin() or OsUtils.isMac():
            self.runtimeDependencies["binary/r-base"] = None
        else:
            self.runtimeDependencies["libs/r-base"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["libs/qt/qtwebengine"] = None
        # not strictly runtimeDependencies, but should be included in the package for plugins and extra functionality
        self.runtimeDependencies["kde/applications/kate"] = None
        if not OsUtils.isMac():
            # kbibtex does not properly build on macOS, yet, and is optional
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
            # Needed at runtime to keep libcurl working inside the AppImage. See definition of CURL_CA_BUNDLE, below.
            self.runtimeDependencies["core/cacert"] = None
            # Needed for building some R packages
            self.runtimeDependencies["dev-utils/sed"] = None
            # tags io-slave used by KEncodingFileDialog (producing ugly warning, if not present)
            self.runtimeDependencies["kde/frameworks/tier3/baloo"] = None
        elif OsUtils.isMac():
            # indirectly required by kate, but not declared as dependency, there
            self.runtimeDependencies["kde/plasma/plasma-activities"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            ]

    def fetch(self):
        if not super().fetch():
            return False
        return True

    def setDefaults(self, defines: {str: str}) -> {str: str}:
        defines = super().setDefaults(defines)
        if OsUtils.isLinux() and isinstance(self, AppImagePackager):
            defines["runenv"].append('CURL_CA_BUNDLE="$this_dir/etc/cacert.pem"')
        return defines

    def install(self):
        ret = super().install()
        if OsUtils.isWin() or OsUtils.isLinux():
            # Make installation movable, by providing rkward.ini with relative path to R
            rkward_ini = open(os.path.join(self.imageDir(), "bin", "rkward.ini"), "w")
            if OsUtils.isLinux():
                rkward_ini.write("R executable=../lib/R/bin/R\n")
            elif OsUtils.isWin():
                rkward_ini.write("R executable=../lib/R/bin/x64/R.exe\n")
            else:
                # On Mac there is no sane way to bundle R along with RKWard, so make the default behavior to detect an R installation, automatically.
                rkward_ini.write("R executable=auto\n")
            rkward_ini.close()
        return ret

    def createPackage(self):
        if OsUtils.isWin() and (not CraftCore.settings.get("Packager", "PackageType", "")):
            self.changePackager("InnoSetupPackager")

        self.defines["executable"] = "bin\\rkward.exe"
        self.defines["icon"] = os.path.join(self.sourceDir(), "rkward", "icons", "app-icon", "rkward.ico")
        self.defines["file_types"] = [".R", ".Rdata", ".Rmd", ".rko"]

        self.ignoredPackages.append("libs/llvm")
        # VLC pulled in indirectly via okular. Removing this saves a bunch
        self.ignoredPackages.append("libs/vlc")
        self.ignoredPackages.append("binary/vlc")

        if OsUtils.isMac():
            # We cannot reliably package R inside the bundle. Users will have to install it separately.
            self.ignoredPackages.append("binary/r-base")
            # Inspired by kate: exclude most binaries
            self.addExecutableFilter(r"(bin|libexec)/(?!(kate|okular|kbibtex|rkward|pandoc|update-mime-database|kioworker)).*")
            # Certain plugin files defeat codesigning on macOS, which is picky about file names -> TODO check/update list
            self.blacklist_file.append(os.path.join(self.blueprintDir(), "blacklist_mac.txt"))

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("data/hunspell-dictionaries")
        self.whitelist_file.append(os.path.join(self.blueprintDir(), "whitelist.txt"))

        return super().createPackage()

    def reinplace(self, filename, old, new):
        CraftCore.log.info(f"patching {old} -> {new} in {filename}")
        with open(filename, "r") as f:
            content = f.read()
        with open(filename, "w") as f:
            f.write(content.replace(old, new))

    def preArchive(self):
        if OsUtils.isLinux() and isinstance(self, AppImagePackager):
            for filename in ["bin/R", "lib/R/bin/R", "lib/R/bin/libtool", "lib/R/etc/ldpaths", "lib/R/etc/Renviron"]:
                filename = os.path.join(self.archiveDir(), filename)
                self.reinplace(filename, str(CraftCore.standardDirs.craftRoot()), "${APPDIR}/usr")
            for filename in ["lib/R/etc/Makeconf"]:
                filename = os.path.join(self.archiveDir(), filename)
                self.reinplace(filename, str(CraftCore.standardDirs.craftRoot()), "$(APPDIR)/usr")  # NOTE: round braces, here
            # quirkaround for making kioworkers work despite of https://github.com/linuxdeploy/linuxdeploy/issues/208 / https://invent.kde.org/packaging/craft/-/merge_requests/80
            for subpath in ["libexec/lib", "lib/libexec/lib", "plugins/lib", "plugins/kf5/lib"]:
                utils.createSymlink(os.path.join(self.archiveDir(), "lib"), os.path.join(self.archiveDir(), subpath), targetIsDirectory=True)
        return super().preArchive()
