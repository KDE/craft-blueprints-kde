import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "A simple, user-friendly Jabber/XMPP client for every device!"
        self.displayName = "Kaidan"

        self.svnTargets['master'] = 'https://anongit.kde.org/kaidan.git'
        for ver in ["0.4.1", "0.5.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/kaidan/{ver}/kaidan-{ver}.tar.xz"
            self.archiveNames[ver] = f"kaidan-v{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kaidan-{ver}"
        self.targetDigests['0.4.1'] = (
            ['a9660e2b9c9d9ac6802f7de9a8e1d29a6d552beffcafca27231682bf1038e03c'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['0.5.0'] = (
            ['0f1d267d9c6001a26056789aa521bd5b0e36eea39dff95d4f33dbcd3e5257247'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '0.5.0'

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtlocation"] = None
        self.runtimeDependencies["libs/zxing-cpp"] = None
        self.runtimeDependencies["qt-libs/qxmpp"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["executable"] = r"bin\kaidan.exe"

        return TypePackager.createPackage(self)
