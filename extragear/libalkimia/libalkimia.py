# -*- coding: utf-8 -*-
# Copyright 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>
# Copyright 2019 Thomas Baumgart <tbaumgart@kde.org>
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

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["7.0.1", "7.0.2", "8.0.1", "8.0.2", "8.0.3", "8.0.4", "8.1.0", "8.1.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/alkimia/{ver}/alkimia-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/alkimia/{ver}/alkimia-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"alkimia-{ver}"

        self.svnTargets["master"] = "https://invent.kde.org/office/alkimia.git"
        self.targetUpdatedRepoUrl["master"] = ("https://anongit.kde.org/alkimia", "https://invent.kde.org/office/alkimia.git")
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        # if self.buildTarget == "master" or self.buildTarget >= CraftVersion("8.0"):
        #    self.runtimeDependencies["libs/qt5/qtwebkit"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["libs/libgmp"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.description = "A library with common classes and functionality used by finance applications for the KDE SC."


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()

        self.subinfo.options.configure.args += ["-DBUILD_APPLETS=OFF", "-DCMAKE_DISABLE_FIND_PACKAGE_Qt5WebEngineWidgets=1"]

    def createPackage(self):
        self.defines["appname"] = "onlinequoteseditor5"
        self.defines["apppath"] = "Applications/KDE/onlinequoteseditor5.app"
        return super().createPackage()
