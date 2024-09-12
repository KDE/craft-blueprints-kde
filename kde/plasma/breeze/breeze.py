import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.versionInfo.tarballs():
            self.patchToApply[ver] = ("breeze-noWinDrag.diff", 0)
            self.patchLevel[ver] = 3

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
        if not CraftCore.compiler.platform.isWindows and not CraftCore.compiler.platform.isMacOS:
            self.runtimeDependencies["kde/frameworks/tier4/frameworkintegration"] = None
            self.runtimeDependencies["kde/plasma/kdecoration"] = None


class Package(CraftPackageObject.get("kde/plasma").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not CraftCore.compiler.platform.isWindows or CraftCore.compiler.platform.isMacOS:
            self.subinfo.options.configure.args += ["-DCMAKE_DISABLE_FIND_PACKAGE_KF6FrameworkIntegration=ON", "-DWITH_DECORATIONS=OFF"]
        self.subinfo.options.configure.args += ["-DBUILD_QT5=OFF"]

    def install(self):
        status = super().install()
        # On Windows files are wrongly installed to "share" while they should go to "bin/data"
        # This fix is to workaround that bug. It should be removed as soon as the bug is fixed
        # See https://invent.kde.org/frameworks/extra-cmake-modules/-/merge_requests/428
        if CraftCore.compiler.platform.isWindows:
            utils.moveFile(self.imageDir() / "share", self.imageDir() / "bin/data")

        for module in ["Breeze"]:
            filename = self.imageDir() / "lib" / "cmake" / module / f"{module}Config.cmake"
            with open(filename, "r") as f:
                contents = f.read()
            with open(filename, "w") as f:
                f.write(contents.replace("share/color-schemes", "bin/data/color-schemes"))

        return status
