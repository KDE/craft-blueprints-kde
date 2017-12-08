import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/skrooge|master'
        for ver in ['2.10.5']:
            self.targets[ver] = 'https://download.kde.org/stable/skrooge/skrooge-' + ver + '.tar.xz'
            self.targetInstSrc[ver] = 'skrooge-%s' % ver
        self.defaultTarget = '2.10.5'
        self.description = "personal finance manager for KDE"

    def setDependencies(self):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qt5/qtsvg"] = "default"
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebengine"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(self.packageDir(), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines["productname"] = "AtCoreTest"
        self.defines["executable"] = "bin\\atcore.exe"
        self.defines["website"] = "https://atelier.kde.org"
        self.defines["icon"] = os.path.join(self.packageDir(), "atcore.ico")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
