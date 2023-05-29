import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Marble"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtlocation"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt5/qtwebchannel"] = None
            self.runtimeDependencies["libs/qt5/qtwebengine"] = None
            self.runtimeDependencies["libs/qt5/qtserialport"] = None
            self.runtimeDependencies["qt-libs/phonon"] = None
            self.runtimeDependencies["libs/protobuf"] = None
        else:
            self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = None
            self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_MARBLE_TESTS=OFF -DWITH_KF5=OFF"

    def createPackage(self):
        self.defines["productname"] = "Marble"
        self.defines["executable"] = "bin\\marble-qt.exe"
        self.defines["icon"] = os.path.join(self.sourceDir(), "data", "ico", "marble.ico")
        self.defines["icon_png"] = os.path.join(self.packageDir(), "150-apps-marble.png")
        self.defines["icon_png_44"] = os.path.join(self.packageDir(), "44-apps-marble.png")
        self.defines["shortcuts"] = [{"name" : "Marble", "target" : "bin\marble-qt.exe"}]
        self.defines["website"] = "https://marble.kde.org/"

        self.addExecutableFilter(r"bin/(?!(marble-qt|QtWebEngineProcess)).*")

        return TypePackager.createPackage(self)
