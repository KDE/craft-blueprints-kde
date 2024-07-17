import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/ktorrent"
        for version in ["4.3.1"]:
            self.targets[version] = "https://ktorrent.org/downloads/" + version + "/ktorrent-" + version + ".tar.bz2"
            self.targetInstSrc[version] = "ktorrent-" + version
        # these patches were pushed upstream, see:
        # https://commits.kde.org/ktorrent/72c0379dc75dcbec878ca2ea940d06f771b38438
        # https://commits.kde.org/ktorrent/aa0060b48afc4f01a4c50a47d0e19047bc4da51e
        self.patchToApply["4.3.1"] = [
            ("0001-Do-not-include-signalcatcher.h-in-windows.patch", 1),
            ("0002-Cast-activateWindow-param-to-improved-portability.patch", 1),
        ]

        self.description = "A powerful BitTorrent client."
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None

        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kstatusnotifieritem"] = None

        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None

        self.runtimeDependencies["kde/libs/libktorrent"] = None

        if CraftCore.compiler.isLinux or CraftCore.compiler.isFreeBSD:
            self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kglobalaccel"] = None

class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
