# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["qt-libs/phonon"] = None
        self.runtimeDependencies["binary/vlc"] = None
        if CraftCore.compiler.isMSVC() or CraftCore.compiler.isIntel():
            self.runtimeDependencies["kdesupport/kdewin"] = None

    def setTargets(self):
        for ver in ["0.10.0", "0.11.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/phonon/phonon-backend-vlc/{ver}/phonon-backend-vlc-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/phonon/phonon-backend-vlc/{ver}/phonon-backend-vlc-{ver}.tar.xz.sha256"
            if CraftVersion(ver) >= "0.11.1":
                self.targetInstSrc[ver] = f"phonon-backend-vlc-{ver}"
            else:
                self.targetInstSrc[ver] = f"phonon-vlc-{ver}"

            self.patchToApply[ver] = [("qtdbus-lib-macos.diff", 1)] # Add patch for link error of QtDBus on macOS

        self.svnTargets["master"] = "https://anongit.kde.org/phonon-vlc"

        self.description = "the vlc based phonon multimedia backend"
        self.defaultTarget = "0.11.1"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = " -DPHONON_BUILD_PHONON4QT5=ON"
