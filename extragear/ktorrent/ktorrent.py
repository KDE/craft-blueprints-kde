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
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["libs/libgmp"] = None
        self.runtimeDependencies["kde/libs/libktorrent"] = None
        self.buildDependencies["libs/gettext"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
