import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Interactive graphing and analysis of scientific data"
        self.displayName = "LabPlot2"

        for ver in ['2.4.0']:
            self.targets[ver] = 'http://download.kde.org/stable/labplot/%s/labplot-%s-kf5.tar.xz' % (ver, ver)
            self.targetInstSrc[ver] = 'labplot-%s-kf5' % ver

        # FIXME: note: 2.4.0 does not build. Wait for a new release.
        # b/c of: cl : Command line error D8021 : invalid numeric argument '/Wextra'
        self.defaultTarget = 'master' # '2.4.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtserialport"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier4/kdelibs4support"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["appname"] = "labplot2"
        self.defines["website"] = "https://labplot.kde.org/"
        self.defines["executable"] = "bin\\labplot2.exe"
        self.defines["shortcuts"] = [{"name" : "LabPlot2", "target":"bin/labplot2.exe", "description" : self.subinfo.description}]
        self.defines["icon"] = os.path.join(self.packageDir(), "labplot2.ico")

        self.defines["mimetypes"] = ["application/x-labplot2"]
        self.defines["file_types"] = [".lml"]

        # ignored files
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))

        return super().createPackage()

