import info
from CraftOS.osutils import OsUtils
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/sdk/heaptrack.git"

        for ver in ["1.4.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/heaptrack/{ver}/heaptrack-{ver}.tar.xz"
            self.targetInstSrc[ver] = "heaptrack-" + ver
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/heaptrack/{ver}/heaptrack-{ver}.tar.xz.sig"

        self.description = "A heap memory profiler for Linux"
        self.webpage = "https://invent.kde.org/sdk/heaptrack"
        self.displayName = "heaptrack"

        self.defaultTarget = "1.4.0"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/boost/boost-headers"] = None

        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/boost/boost-system"] = None
        self.runtimeDependencies["libs/boost/boost-program-options"] = None
        self.runtimeDependencies["libs/boost/boost-iostreams"] = None
        self.runtimeDependencies["libs/boost/boost-filesystem"] = None
        self.runtimeDependencies["libs/boost/boost-container"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/elfutils"] = None
        self.runtimeDependencies["libs/libunwind"] = None
        self.runtimeDependencies["libs/libzstd"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DAPPIMAGE_BUILD=ON"]

    def createPackage(self):
        self.blacklist_file.append(self.packageDir() / "blacklist.txt")

        # override AppRun behavior in AppImage point

        # - update PATH to ensure we find heaptrack_gui
        # - run heaptrack instead of heaptrack_gui as entry
        # - then don't continue, or we would run the normal AppRun.wrapped,
        #   which would point at heaptrack_gui
        self.defines["runenv"] = [
            'PATH="$this_dir/usr/bin:$PATH"; "$this_dir/usr/bin/heaptrack" "$@"; exit;'
        ]

        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")

        return super().createPackage()

    def preArchive(self):
        if CraftCore.compiler.isLinux:
            # --- Manage files under AppImage bundle

            packageDir = self.packageDir()
            archiveDir = self.archiveDir()

            print(packageDir, archiveDir)

            # Replace heaptrack_gui with script to setup env

            if not utils.moveFile(os.path.join(archiveDir, "bin/heaptrack_gui"), os.path.join(archiveDir, "bin/heaptrack_gui.wrapped")):
                return False

            # add custom wrapper script

            if not utils.copyFile(os.path.join(packageDir, "heaptrack_gui.wrapper"), os.path.join(archiveDir, "bin/heaptrack_gui")):
                return False

        return True
