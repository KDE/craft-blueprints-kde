import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "A BitTorrent protocol implementation."

    def setDependencies(self):
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["libs/libgmp"] = None
        self.runtimeDependencies["libs/gpgme"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.buildDependencies["libs/gettext"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
