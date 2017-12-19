import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/skrooge|master'
        for ver in ['2.10.5']:
            self.targets[ver] = 'https://download.kde.org/stable/skrooge/skrooge-' + ver + '.tar.xz'
            self.targetInstSrc[ver] = 'skrooge-%s' % ver
        self.targetDigests['2.10.5'] = (['56a0124dec34e6e96a5e71ff0e825a7ec79f32a69ef0ccdc5f0f9b753d8c3eb0'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '2.10.5'
        self.description = "personal finance manager for KDE"

    def setDependencies(self):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qt5/qtsvg"] = "default"
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebkit"] = "default"
        self.runtimeDependencies["frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["frameworks/tier3/knewstuff"] = "default"
        self.runtimeDependencies["frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["frameworks/tier3/kwallet"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["kdesupport/grantlee"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        #self.subinfo.options.configure.args = "-DSKG_WEBENGINE=ON"
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            #os.path.join(self.packageDir(), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines["productname"] = "Skrooge"
        self.defines["website"] = "https://skrooge.org/"
        #self.defines["icon"] = os.path.join(self.packageDir(), "skrooge.ico")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
