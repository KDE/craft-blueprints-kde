import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        # add backported patch for 5.83.0 to allow inline-replies on Windows Notifications
        if CraftCore.compiler.isWindows:
            self.patchToApply["5.83.0"] = [("inline_reply_win_backported.diff", 1)]
            self.patchLevel["5.83.0"] = 1

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt5/qtspeech"] = None
            self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
            self.runtimeDependencies["qt-libs/phonon"] = None
        else:
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = None
        if OsUtils.isMac():
            self.runtimeDependencies["libs/qt5/qtmacextras"] = None
        if OsUtils.isWin():
            self.runtimeDependencies["dev-utils/snoretoast"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
