import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.versionInfo.tarballs():
            self.patchToApply[ver] = ("breeze-noWinDrag.diff", 0)

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpackage"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        if not OsUtils.isWin():
            self.runtimeDependencies["kde/frameworks/tier4/frameworkintegration"] = None
        if not OsUtils.isWin() and not OsUtils.isMac():
            self.runtimeDependencies["kde/plasma/kdecoration"] = None


class Package(CraftPackageObject.get("kde/plasma").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if OsUtils.isWin():
            self.subinfo.options.configure.args += ["-DCMAKE_DISABLE_FIND_PACKAGE_KF5FrameworkIntegration=ON", "-DWITH_DECORATIONS=OFF"]

        if OsUtils.isMac():
            self.subinfo.options.configure.args += ["-DWITH_DECORATIONS=OFF"]
        self.subinfo.options.configure.args += f"-DBUILD_QT5=OFF"

    def install(self):
        status = super().install()
        # On Windows files are wrongly installed to "share" while they should go to "bin/data"
        # This fix is to workaround that bug. It should be removed as soon as the bug is fixed
        # See https://invent.kde.org/frameworks/extra-cmake-modules/-/merge_requests/428
        utils.moveFile(self.imageDir() / "share", self.imageDir() / "bin/data")

        for module in ["Breeze"]:
            filename = self.imageDir() / "lib" / "cmake" / module / f"{module}Config.cmake"
            with open(filename, "r") as f:
                contents = f.read()
            with open(filename, "w") as f:
                f.write(contents.replace(f"share/color-schemes", f"bin/data/color-schemes"))

        return status
