import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


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

        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/boost"] = None
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DAPPIMAGE_BUILD=ON"]

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")

        # override AppRun behavior in AppImage point

        # - update PATH to ensure we find heaptrack_gui
        # - run heaptrack instead of heaptrack_gui as entry
        # - then don't continue, or we would run the normal AppRun.wrapped,
        #   which would point at heaptrack_gui
        self.defines["runenv"] = ['PATH="$this_dir/usr/bin:$PATH"; "$this_dir/usr/bin/heaptrack" "$@"; exit;']

        if not CraftCore.compiler.platform.isLinux:
            self.ignoredPackages.append("libs/dbus")

        return super().createPackage()

    def preArchive(self):
        if CraftCore.compiler.platform.isLinux:
            # --- Manage files under AppImage bundle

            packageDir = self.blueprintDir()
            archiveDir = self.archiveDir()

            print(packageDir, archiveDir)

            # Replace heaptrack_gui with script to set up the env

            if not utils.moveFile(archiveDir / "bin/heaptrack_gui", archiveDir / "bin/heaptrack_gui.wrapped"):
                return False

            # add custom wrapper script

            if not utils.copyFile(packageDir / "heaptrack_gui.wrapper", archiveDir / "bin/heaptrack_gui"):
                return False

        return True
