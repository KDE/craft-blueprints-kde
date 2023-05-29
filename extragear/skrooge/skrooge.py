import info
from Packager.CollectionPackagerBase import PackagerLists


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/skrooge|master"
        for ver in ["2.27.0"]:
            self.targets[ver] = "https://download.kde.org/stable/skrooge/skrooge-" + ver + ".tar.xz"
            self.targetInstSrc[ver] = "skrooge-%s" % ver
        self.targetDigests["2.27.0"] = (["c649745322440ce7983aaa977f7c2808331bf19c82d9ce428507431451116711"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.27.0"
        self.description = "personal finance manager for KDE"
        self.displayName = "Skrooge"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = None
        self.runtimeDependencies["libs/qt5/qtwebkit"] = None
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


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        # self.subinfo.options.configure.args = "-DSKG_WEBENGINE=ON"
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            # os.path.join(self.packageDir(), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines["website"] = "https://skrooge.org/"
        # self.defines["icon"] = os.path.join(self.packageDir(), "skrooge.ico")

        return TypePackager.createPackage(self)
