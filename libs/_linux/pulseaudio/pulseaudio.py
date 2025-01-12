# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "PulseAudio is a sound server system for POSIX OSes, meaning that it is a proxy for your sound applications."

        for ver in ["16.99.1"]:
            self.targets[ver] = f"https://www.freedesktop.org/software/pulseaudio/releases/pulseaudio-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"pulseaudio-{ver}"

        self.patchLevel["16.99.1"] = 4
        self.targetDigests["16.99.1"] = (["ba02fa11e7e2b78555ad16525448fa165c03d5ff99e2f09eb49e0b7e1038b388"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "16.99.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None
        self.buildDependencies["perl-modules/xml-parser"] = None
        self.runtimeDependencies["libs/libsndfile"] = None
        self.runtimeDependencies["dev-utils/libtool"] = None  # For libltdl


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-Ddatabase=simple", "-Dx11=disabled", "-Dtests=false", "-Ddoxygen=false"]
        self.subinfo.options.configure.ldflags += " -lintl"
        self.subinfo.options.package.disableBinaryCache = True
