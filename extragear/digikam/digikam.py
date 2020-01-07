# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'git://anongit.kde.org/digikam.git'
        self.defaultTarget = 'master'

        self.displayName = "digiKam"
        self.webpage = "https://www.digikam.org"
        self.description = "Professional Photo Management with the Power of Open Source"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["binary/mysql"] = None
        self.runtimeDependencies['libs/x265'] = None
        self.runtimeDependencies['libs/tiff'] = None
#        self.runtimeDependencies['libs/boost'] = None # do not force boost deps (see: https://phabricator.kde.org/T12071#212690)
        self.runtimeDependencies['libs/expat'] = None
        self.runtimeDependencies['libs/ffmpeg'] = None
        self.runtimeDependencies['libs/lcms2'] = None
        self.runtimeDependencies['libs/eigen3'] = None
        self.runtimeDependencies['libs/exiv2'] = None
        self.runtimeDependencies['libs/opencv'] = None
        self.runtimeDependencies['libs/lensfun'] = None
        self.runtimeDependencies['libs/libpng'] = None
        self.runtimeDependencies['libs/libxslt'] = None
        self.runtimeDependencies['libs/libxml2'] = None
        self.runtimeDependencies['libs/openal-soft'] = None
        self.runtimeDependencies['libs/pthreads'] = None
        self.runtimeDependencies['libs/libjpeg-turbo'] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtimageformats"] = None
        self.runtimeDependencies["libs/qt5/qtxmlpatterns"] = None
        self.runtimeDependencies["libs/qt5/qtwebengine"] = None
        self.runtimeDependencies['kde/frameworks/tier1/kconfig'] = None
        self.runtimeDependencies['kde/frameworks/tier3/kxmlgui'] = None
        self.runtimeDependencies['kde/frameworks/tier1/ki18n'] = None
        self.runtimeDependencies['kde/frameworks/tier1/kwindowsystem'] = None
        self.runtimeDependencies['kde/frameworks/tier1/breeze-icons'] = None
        self.runtimeDependencies['kde/frameworks/tier3/kservice'] = None
        self.runtimeDependencies['kde/frameworks/tier1/solid'] = None
        self.runtimeDependencies['kde/frameworks/tier1/kcoreaddons'] = None
        self.runtimeDependencies['kde/frameworks/tier1/threadweaver'] = None
        self.runtimeDependencies['kde/frameworks/tier3/kiconthemes'] = None
        self.runtimeDependencies['kde/frameworks/tier1/kcalendarcore'] = None
        #self.runtimeDependencies["kde/applications/marble"] = None

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["productname"] = "digiKam"
        self.defines["website"] = "https://www.digikam.org"
        self.defines["executable"] = "bin\\digikam.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "digikam.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
