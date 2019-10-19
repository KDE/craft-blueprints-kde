import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/kile'
        self.svnTargets['gitStable-2.1'] = 'git://anongit.kde.org/kile|2.1|'
        for ver in ['2.1.1', '2.9.92', '2.9.93']:
            self.targets[ver] = 'http://downloads.sourceforge.net/kile/kile-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'kile-' + ver
        self.description = "a user friendly TeX/LaTeX editor for KDE"
        self.displayName = "Kile"
        self.webpage = "https://kile.sourceforge.io/"
        self.defaultTarget = '2.9.93'

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtscript"] = None
        self.runtimeDependencies['qt-libs/poppler'] = 'default'
        self.runtimeDependencies['kde/applications/okular'] = 'default'
        self.runtimeDependencies["kde/applications/kate"] = None
        self.runtimeDependencies["kde/frameworks/tier3/khtml"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.defines["executable"] = "bin\\kile.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kile.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
