# -*- coding: utf-8 -*-
# Copyright (c) 2019-2020 by Gilles Caulier <caulier dot gilles at gmail dot com>
# Copyright (c) 2019-2020 by Ben Cooksley <bcooksley at kde dot org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# NOTE: see relevant phabricator entry https://phabricator.kde.org/T12071

import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://anongit.kde.org/digikam.git'
        self.defaultTarget = 'master'
        self.displayName = "digiKam"
        self.webpage = "https://www.digikam.org"
        self.description = "Professional Photo Management with the Power of Open Source"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.buildDependencies['libs/ffmpeg'] = "4.4"
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies['libs/x265'] = None
        self.runtimeDependencies['libs/tiff'] = None
#        self.runtimeDependencies['libs/boost/boost-system'] = "default"
#        self.runtimeDependencies['libs/boost'] = None # do not force boost deps (see: https://phabricator.kde.org/T12071#212690)
        self.runtimeDependencies['libs/expat'] = None
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
        self.runtimeDependencies["libs/_autotools/libass"] = None
        if CraftCore.compiler.isMinGW():
            self.runtimeDependencies["libs/qt5/qtwebkit"] = None
        else:
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
        #self.runtimeDependencies["kde/applications/marble"] = None # See marble.py: there is no rules to share Marble widgets yet.

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args = " -DENABLE_KFILEMETADATASUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_AKONADICONTACTSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MEDIAPLAYER=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DBUS=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_QWEBENGINE=ON"
            self.subinfo.options.configure.args += f" -DENABLE_MYSQLSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_INTERNALMYSQL=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DIGIKAM_MODELTEST=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DRMINGW=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MINGW_HARDENING_LINKER=OFF"
            self.subinfo.options.configure.args += f" -DBUILD_TESTING=OFF"

        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.args = " -DENABLE_KFILEMETADATASUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_AKONADICONTACTSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MEDIAPLAYER=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DBUS=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_QWEBENGINE=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MYSQLSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_INTERNALMYSQL=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DIGIKAM_MODELTEST=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DRMINGW=ON"
            self.subinfo.options.configure.args += f" -DENABLE_MINGW_HARDENING_LINKER=ON"
            self.subinfo.options.configure.args += f" -DBUILD_TESTING=OFF"

        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args = " -DENABLE_KFILEMETADATASUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_AKONADICONTACTSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MEDIAPLAYER=ON"
            self.subinfo.options.configure.args += f" -DENABLE_DBUS=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_QWEBENGINE=ON"
            self.subinfo.options.configure.args += f" -DENABLE_MYSQLSUPPORT=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_INTERNALMYSQL=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DIGIKAM_MODELTEST=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_DRMINGW=OFF"
            self.subinfo.options.configure.args += f" -DENABLE_MINGW_HARDENING_LINKER=OFF"
            self.subinfo.options.configure.args += f" -DBUILD_TESTING=OFF"

    def createPackage(self):
        self.defines["productname"] = "digiKam"
        self.defines["website"] = "https://www.digikam.org"
        self.defines["company"] = "digiKam.org"
        self.defines["executable"] = "bin\\digikam.exe"                         # Windows-only, mac is handled implicitly
        self.defines["icon"] = os.path.join(self.packageDir(), "digikam.ico")   # Windows-only
        self.defines["shortcuts"] = [{"name" : "digiKam", "target":"bin/digikam.exe", "description" : self.subinfo.description, "icon" : "$INSTDIR\\digikam.ico" }]     # Windows-only

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
