import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "A simple, user-friendly Jabber/XMPP client for every device!"
        self.displayName = "Kaidan"

        self.svnTargets['master'] = 'https://anongit.kde.org/kaidan.git'
        for ver in ["0.6.0"]:
            self.targets[ver] = f"https://download.kde.org/unstable/kaidan/{ver}/kaidan-{ver}.tar.xz"
            self.archiveNames[ver] = f"kaidan-v{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kaidan-{ver}"
        self.targetDigests['0.6.0'] = (
            ['7b9008b9fcb5ff2de47ac40eaf64c97a5652e756f0eb32306f6ad1320ce52ee7'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '0.6.0'

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
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), 'excludelist_mac.txt'))

        self.defines["executable"] = r"bin\kaidan.exe"

        return TypePackager.createPackage(self)
