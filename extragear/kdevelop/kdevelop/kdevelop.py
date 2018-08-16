from distutils.dir_util import mkpath

import info
from Blueprints.CraftVersion import CraftVersion


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "KDE Integrated Development Environment for C/C++/QML/JS/Python/PHP/..."
        self.webpage = "https://kdevelop.org"
        self.displayName = "KDevelop"

    def registerOptions(self):
        self.options.dynamic.registerOption("fullKDevelop", False)
        self.options.dynamic.registerOption("fullPlasma", False)

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-utils/7zip"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebkit"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kinit"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["kde/kdesdk/libkomparediff2"] = "default"
        self.runtimeDependencies["data/hicolor-icon-theme"] = "default"
        self.runtimeDependencies["libs/llvm-meta/clang"] = "default"

        # handle kdevplatform merge into kdevelop.git
        if self.buildTarget != "master" and CraftVersion(self.buildTarget) < CraftVersion("5.2"):
            self.runtimeDependencies["extragear/kdevelop/kdevplatform"] = "default"
        else:
            self.runtimeDependencies["libs/qt5/qtquickcontrols"] = "default"
            self.runtimeDependencies["libs/qt5/qtwebengine"] = "default"
            self.runtimeDependencies["kdesupport/grantlee"] = "default"

        if self.options.dynamic.fullPlasma:
            self.runtimeDependencies["kde/frameworks/tier3/krunner"] = "default"
            self.runtimeDependencies["kde/frameworks/tier3/plasma-framework"] = "default"
        if self.options.dynamic.fullKDevelop:
            self.packagingDependencies["extragear/kdevelop/kdev-python"] = "default"
            self.packagingDependencies["extragear/kdevelop/kdev-php"] = "default"
        self.runtimeDependencies["extragear/kdevelop-pg-qt"] = "default"

        # Install extra plugins shipped by Kate
        self.runtimeDependencies["kde/applications/kate"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.packageDir(), 'blacklist.txt'))
        self.defines["shortcuts"] = [{"name" : "KDevelop", "target" : "bin/kdevelop.exe"},
                                     {"name" : "KDevelop - Microsoft Visual C++ compiler", "target":"bin/kdevelop-msvc.bat"}]
        self.defines["icon"] = os.path.join(self.packageDir(), "kdevelop.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
