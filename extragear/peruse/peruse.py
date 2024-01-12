import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/peruse|master"
        self.defaultTarget = "master"
        self.description = "Peruse Comic Book Viewer and Creator"
        self.webpage = "http://peruse.kde.org"
        self.displayName = "Peruse Comic Book Viewer"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/kdenetwork/kio-extras"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        self.runtimeDependencies["kde/applications/okular"] = None


from Package.CMakePackageBase import *
from Packager.AppImagePackager import AppImagePackager


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.fetch.checkoutSubmodules = True

    def setDefaults(self, defines: {str: str}) -> {str: str}:
        defines = super().setDefaults(defines)
        if OsUtils.isLinux() and isinstance(self, AppImagePackager):
            defines["runenv"] += ["LD_LIBRARY_PATH=$this_dir/usr/lib/:$LD_LIBRARY_PATH"]
        return defines

    def createPackage(self):
        self.defines["shortcuts"] = [
            {"name": self.subinfo.displayName, "target": "bin//peruse.exe"},
            {"name": "Peruse Creator", "target": "bin//perusecreator.exe"},
        ]
        self.defines["icon"] = os.path.join(os.path.dirname(__file__), "peruse.ico")
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")

        return super().createPackage()
