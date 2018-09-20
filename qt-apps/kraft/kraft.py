import info
import os

import io
import re

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["master"]:
            self.svnTargets[ver] = f"[git]https://github.com/owncloud/client|{ver}|"

        self.defaultTarget = 'master'
        self.description = "ownCloud Desktop Client"
        self.webpage = "https://owncloud.org"

    def setDependencies(self):
        self.buildDependencies["craft/craft-blueprints-owncloud"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/cmake"] = None
        self.runtimeDependencies["libs/ctemplate"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = None
        self.runtimeDependencies["kde/pim/kcontacts"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True

    def createPackage(self):
        self.defines["shortcuts"] = [{"name" : "Owncloud Client", "target":"bin/owncloud.exe", "description" : self.subinfo.description}]
        return TypePackager.createPackage(self)
