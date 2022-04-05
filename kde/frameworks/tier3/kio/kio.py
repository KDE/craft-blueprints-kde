import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.90.0"] = [("0001-Port-to-KLibexec.patch", 1)]
        self.patchToApply["5.90.0"] += [("0001-Fix-appimage-build.patch", 1)]
        if CraftCore.compiler.isMinGW():
            self.patchToApply["5.90.0"] += [("fix-mingw.patch", 1)]
            self.patchToApply["5.91.0"] = [("fix-mingw.patch", 1)]
            self.patchToApply["5.92.0"] = [("fix-mingw.patch", 1)]
            self.patchToApply["5.92.0"] += [("fix-mingw-qstandardpath-include.diff", 1)]
        self.patchLevel["5.90.0"] = 5
        self.patchLevel["5.91.0"] = 51
        self.patchLevel["5.92.0"] = 2

        self.description = "Network transparent access to files and data"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
            self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None

        if CraftCore.compiler.isLinux or CraftCore.compiler.isFreeBSD:
            self.runtimeDependencies["kde/frameworks/tier3/kded"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += f" -DKIO_ASSERT_SLAVE_STATES={'ON' if self.buildType() == 'Debug' else 'OFF'}"
        self.subinfo.options.configure.args += " -DCMAKE_DISABLE_FIND_PACKAGE_KF5DocTools=ON "
        if OsUtils.isWin() or OsUtils.isMac():
            self.subinfo.options.configure.args += " -DKIO_FORK_SLAVES=ON "

    def configure(self):
        cfg = CMakePackageBase.configure(self)
        if not cfg and CraftCore.compiler.isLinux:
            CraftCore.log.info("You may need to install libmount-dev(el) and blkid-dev(el) on builder")
        return cfg

