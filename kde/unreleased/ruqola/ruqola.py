# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
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
        self.displayName = "Ruqola"
        self.description = "Rocket.Chat Client"
        self.webpage = "https://apps.kde.org/ruqola"

        self.targets["2.0.0"] = "https://download.kde.org/stable/ruqola/ruqola-2.0.0.tar.xz"
        self.targetDigests["2.0.0"] = (["a9649936adc3589c1e3a19a921c4b2a54bb6c4f9ffa1af50c7c02cae9f441737"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["2.0.0"] = "ruqola-2.0.0"
        self.svnTargets["master"] = "https://invent.kde.org/network/ruqola.git"
        self.defaultTarget = "2.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtwebsockets"] = None
        self.runtimeDependencies["libs/qt/qtnetworkauth"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt/qtimageformats"] = None
        self.runtimeDependencies["libs/qt/qtspeech"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/purpose"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        self.runtimeDependencies["kde/frameworks/tier1/prison"] = None

        # KUserFeedback yet not an official tier1 framework
        self.runtimeDependencies["kde/unreleased/kuserfeedback"] = None

        self.runtimeDependencies["kde/frameworks/tier1/kidletime"] = None
        self.runtimeDependencies["kde/libs/ktextaddons"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.blacklist_file.append(os.path.join(self.blueprintDir(), "blacklist.txt"))
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.blueprintDir(), "blacklist_mac.txt"))
        self.addExecutableFilter(r"bin/(?!(ruqola|update-mime-database|kio|dbus|snoretoast)).*")
        self.defines["shortcuts"] = [{"name": "Ruqola", "target": "bin/ruqola.exe", "description": self.subinfo.description, "appId": "ruqola"}]

        self.defines["icon"] = os.path.join(self.buildDir(), "src", "apps", "appIcons.ico")

        self.defines["icon_png"] = os.path.join(self.blueprintDir(), "150-apps-ruqola.png")
        self.defines["icon_png_44"] = os.path.join(self.blueprintDir(), "44-apps-ruqola.png")
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
