import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/kmymoney|master'
        self.svnTargets['5.0'] = 'git://anongit.kde.org/kmymoney|5.0'
        self.description = "a personal finance manager for KDE"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier3/kdewebkit"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["frameworks/tier3/kactivities"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemmodels"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemviews"] = "default"
        self.runtimeDependencies["frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["frameworks/tier3/kwallet"] = "default"
        self.runtimeDependencies["frameworks/tier3/knotifications"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktextwidgets"] = "default"
        # self.runtimeDependencies['testing/gpgmepp'] = 'default'
        self.runtimeDependencies["kde/pim/kholidays"] = "default"
        self.runtimeDependencies["kde/pim/kcontacts"] = "default"
        self.runtimeDependencies["kde/pim/kidentitymanagement"] = "default"
        # self.runtimeDependencies["kde/pim/akonadi"] = "default"
        self.runtimeDependencies["binary/mysql"] = "default"
        self.runtimeDependencies["libs/sqlite"] = "default"
        self.runtimeDependencies["libs/libofx"] = "default"
        self.runtimeDependencies["libs/libical"] = "default"
        self.runtimeDependencies["libs/gettext"] = "default"
        self.runtimeDependencies["extragear/libalkimia"] = "default"
        self.runtimeDependencies["extragear/kdiagram"] = "default"
        self.buildDependencies["win32libs/gettext"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebkit"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines["productname"] = "KMyMoney"
        self.defines["executable"] = "bin\\kmymoney.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kmymoney.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

