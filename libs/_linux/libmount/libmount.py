# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.37.4"]:
            # same as provided by alma9
            self.targets[ver] = f"https://www.kernel.org/pub/linux/utils/util-linux/v{ver[:4]}/util-linux-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"util-linux-{ver}"
        self.targetDigests["2.37.4"] = (["634e6916ad913366c3536b6468e7844769549b99a7b2bf80314de78ab5655b83"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.37.4"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += [
            "--disable-all-programs",
            "--disable-bash-completion",
            "--disable-asciidoc",
            "--disable-poman",
            "--without-systemd",
            "--without-python",
            "--enable-libblkid",
            "--enable-libmount",
            "--disable-pylibmount",
        ]
