import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Kaidan"
        self.description = "User-friendly and modern chat app for every device"
        self.webpage = "https://www.kaidan.im/"

        self.svnTargets["master"] = "https://invent.kde.org/network/kaidan.git"
        for ver in ["0.8.0"]:
            self.targets[ver] = f"https://download.kde.org/unstable/kaidan/{ver}/kaidan-{ver}.tar.xz"
            self.archiveNames[ver] = f"kaidan-v{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kaidan-{ver}"

        self.targetDigests["0.8.0"] = (["a7e772dc7abab565fdf9a7bdaf575a6229bdd509de0891079a83bd32766bb1a4"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["libs/zxing-cpp"] = None
        self.runtimeDependencies["qt-libs/qxmpp"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/libs/kquickimageeditor"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None

        if not CraftCore.compiler.platform.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.fetch.checkoutSubmodules = True

    def createPackage(self):
        if CraftCore.compiler.platform.isMacOS:
            self.blacklist_file.append(os.path.join(self.blueprintDir(), "excludelist_mac.txt"))

        self.defines["executable"] = r"bin\kaidan.exe"

        return super().createPackage()
