import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        for ver in ["19.12.0", "19.12.1"]:
            self.patchToApply[ver] = [('cantor-19.12.0-MSVC-libmarkdown.diff', 1)]
        for ver in ["19.12.1"]:
            self.patchToApply[ver] += [('cantor-19.12.1-Windows.diff', 1)]

        self.description = "Cantor"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/png2ico"] = None
        #self.runtimeDependencies["dev-utils/python3"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["qt-libs/poppler"] = None
        # R backend fails compiling with MSVC
        if not CraftCore.compiler.isMSVC():
            self.runtimeDependencies["binary/r-base"] = None
        #self.runtimeDependencies["binary/python-libs"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpty"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/applications/analitza"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.make.supportsMultijob = False

        if OsUtils.isWin():
            self.r_dir = os.path.join(CraftCore.standardDirs.craftRoot(), "lib", "R", "bin", "x64")
            self.subinfo.options.configure.args = "-DR_EXECUTABLE=" + OsUtils.toUnixPath(os.path.join(self.r_dir, "R.exe"))
            self.subinfo.options.configure.args += " -DR_R_LIBRARY=" + OsUtils.toUnixPath(os.path.join(self.r_dir, "R.dll"))

        pythonPath = CraftCore.settings.get("Paths", "PYTHON")
        self.subinfo.options.configure.args += f" -DPYTHONLIBS3_LIBRARY={pythonPath}"
