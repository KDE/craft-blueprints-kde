import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.75.0"] = [("6324f834e991ace73a07503877420c7ec44e49c1.patch", 1)]

        self.description = "Breeze icon theme."

    def registerOptions(self):
        self.options.dynamic.registerOption("useBreezeDark", False)
        self.options.dynamic.registerOption("useIconResource", OsUtils.isWin() or OsUtils.isMac())

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["python-modules/lxml"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if self.subinfo.options.dynamic.useIconResource:
            self.subinfo.options.configure.args = " -DBINARY_ICONS_RESOURCE=ON -DSKIP_INSTALL_ICONS=ON"

    def install(self):
        if not CMakePackageBase.install(self):
            return False
        if self.subinfo.options.dynamic.useIconResource:
            if CraftCore.compiler.isWindows:
                dest = os.path.join(self.installDir(), "bin", "data")
            else:
                dest = os.path.join(self.installDir(), "share")
            if not os.path.exists(dest):
                os.makedirs(dest)
            if not self.subinfo.options.dynamic.useBreezeDark:
                theme = os.path.join(self.buildDir(), "icons", "breeze-icons.rcc")
            else:
                theme = os.path.join(self.buildDir(), "icons-dark", "breeze-icons-dark.rcc")

            return utils.copyFile(theme, os.path.join(dest, "icontheme.rcc"))
        else:
            return True
