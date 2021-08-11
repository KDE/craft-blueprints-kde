import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "A simple, user-friendly Jabber/XMPP client for every device!"
        self.displayName = "Kaidan"

        self.svnTargets['master'] = 'https://anongit.kde.org/kaidan.git'
        for ver in ["0.7.0"]:
            self.targets[ver] = f"https://download.kde.org/unstable/kaidan/{ver}/kaidan-{ver}.tar.xz"
            self.archiveNames[ver] = f"kaidan-v{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kaidan-{ver}"
            self.patchToApply[ver] = [("704a72a9f0f5c27dbd36ac04e20273c9480dde2a.patch", 1)]

        self.targetDigests['0.7.0'] = (
            ['d56b3c927505adbbe343aa0858599bdbb5322a3ac2bb61dbadffa19428b2304f'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = 'master'

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

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        self.subinfo.options.fetch.checkoutSubmodules = True

    def createPackage(self):
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), 'excludelist_mac.txt'))

        self.defines["executable"] = r"bin\kaidan.exe"

        return TypePackager.createPackage(self)
