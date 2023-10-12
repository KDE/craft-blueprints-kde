# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "PulseAudio is a sound server system for POSIX OSes, meaning that it is a proxy for your sound applications."

        for ver in ["16.99.1"]:
            self.targets[ver] = f"https://freedesktop.org/software/pulseaudio/releases/pulseaudio-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"pulseaudio-{ver}"

        self.patchLevel["16.99.1"] = 2
        self.targetDigests["16.99.1"] = (["ba02fa11e7e2b78555ad16525448fa165c03d5ff99e2f09eb49e0b7e1038b388"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "16.99.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["perl-modules/xml-parser"] = None
        self.runtimeDependencies["libs/libsndfile"] = None


from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-Ddatabase=simple", "-Dx11=disabled", "-Dtests=false", "-Ddoxygen=false"]
        self.subinfo.options.package.disableBinaryCache = True
        self.subinfo.options.configure.ldflags = " ".join(
            [f"-Wl,-rpath,'$ORIGIN/../lib/pulseaudio'", f"-Wl,-rpath,'$ORIGIN/../pulseaudio'", f"-Wl,-rpath,'$ORIGIN/../../pulseaudio'"]
        )
