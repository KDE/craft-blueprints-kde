import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/skrooge|master"
        for ver in ["2.27.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/skrooge/skrooge-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"skrooge-{ver}"
        self.targetDigests["2.27.0"] = (["c649745322440ce7983aaa977f7c2808331bf19c82d9ce428507431451116711"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.27.0"
        self.description = "personal finance manager for KDE"
        self.displayName = "Skrooge"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kdesupport/grantlee"] = None
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["libs/sqlcipher"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.subinfo.options.configure.args = "-DSKG_WEBENGINE=ON"

    def createPackage(self):
        self.defines["website"] = "https://skrooge.org/"
        # self.defines["icon"] = self.blueprintDir() / "skrooge.ico"

        return super().createPackage()
