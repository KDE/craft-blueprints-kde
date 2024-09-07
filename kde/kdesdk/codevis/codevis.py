import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Codevis is a software to visualize large software architectures."
        self.displayName = "Codevis"
        self.webpage = "https://invent.kde.org/sdk/codevis"
        self.svnTargets["master"] = "https://invent.kde.org/sdk/codevis.git"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/runtime"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/llvm"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libzip"] = None
        self.runtimeDependencies["libs/boost"] = None
        self.runtimeDependencies["libs/catch2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ktexttemplate"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["libs/python"] = None

        # try to use Breeze style as Windows style has severe issues for e.g. scaling
        self.runtimeDependencies["kde/plasma/breeze"] = None


# This is needed for the CI
class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += ["-DUSE_QT_WEBENGINE=OFF ", "-DCOMPILE_TESTS=OFF ", f"-DPython_ROOT_DIR={CraftCore.standardDirs.craftRoot()}"]

    def createPackage(self):
        # This is Mac Only
        self.defines["appname"] = "codevis_desktop"

        # This is windows only.
        self.defines["executable"] = "bin\\codevis_desktop.exe"
        self.defines["shortcuts"] = [{"name": "Codevis", "target": "bin/codevis_desktop.exe", "description": self.subinfo.description}]

        # we have multiple codevis executables, we need to copy all of them.
        self.addExecutableFilter(r"bin/(?!((codevis*)|kbuildsycoca5|update-mime-database|kioworker)).*")

        self.defines["file_types"] = [".lks"]
        self.defines["alias"] = "codevis"

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("dev-utils/sed")
        return super().createPackage()
