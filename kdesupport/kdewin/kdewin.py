import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Windows
        self.options.dynamic.registerOption("buildWithQt", False)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        # will be moved to kdewin-qt
        if self.options.dynamic.buildWithQt:
            self.runtimeDependencies["libs/qt/qtbase"] = None
            self.runtimeDependencies["libs/qt/qtsvg"] = None
        # will be moved to kdewin-tools
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libpng"] = None

    def setTargets(self):
        self.svnTargets["0.3.9"] = "http://gitweb.kde.org/kdewin.git/snapshot/fc116df1dc204d8a06dc5c874a4cdecc335115ec.tar.gz"
        self.svnTargets["master"] = "https://invent.kde.org/packaging/kdewin.git"
        for i in ["4.3.0", "4.3.1", "4.3.2", "4.3.3", "4.3.4", "4.3"]:
            self.svnTargets[i] = "tags/kdesupport-for-4.3/kdesupport/kdewin"
        for ver in ["0.5.6"]:
            self.targets[ver] = f"http://www.winkde.org/pub/kde/ports/win32/repository/other/kdewin-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kdewin-{ver}"
        self.patchToApply["0.5.6"] = [("kdewin-0.5.6-20130530.diff", 1), ("invert-if-msvc.diff", 1)]
        self.description = "kde supplementary package for win32"
        self.defaultTarget = "master"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # required for package generating because we build from svnHEAD by default
        #        self.subinfo.options.package.version = '0.5.4'
        self.subinfo.options.configure.args += ["-DBUILD_PNG2ICO=OFF"]
        if not self.subinfo.options.dynamic.buildWithQt:
            self.subinfo.options.configure.args += ["-DBUILD_BASE_LIB_WITH_QT=OFF", "-DBUILD_QT_LIB=OFF"]
        self.subinfo.options.configure.args += ["-DBUILD_TOOLS=ON"]
        if CraftCore.compiler.isMinGW_W32():
            self.subinfo.options.configure.args += ["-DMINGW_W32=ON"]
        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.args += ['-DKDEWIN_DEFINITIONS="-DKDEWIN_NO_LOCALTIME_R -DKDEWIN_NO_GMTIME_R"']
