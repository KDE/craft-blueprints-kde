# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>
import info
import utils
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.4.7"]:
            self.targets[ver] = f"https://github.com/OpenPrinting/cups/releases/download/v{ver}/cups-{ver}-source.tar.gz"
            self.targetInstSrc[ver] = f"cups-{ver}"
        self.targetDigests["2.4.7"] = (["dd54228dd903526428ce7e37961afaed230ad310788141da75cebaa08362cf6c"], CraftHash.HashAlgorithm.SHA256)

        self.description = "The Common Unix Printing System"

        self.defaultTarget = "2.4.7"

    def setDependencies(self):
        self.buildDependencies["dev-utils/automake"] = None
        self.buildDependencies["dev-utils/autoconf"] = None
        self.buildDependencies["dev-utils/pkgconf"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/dbus"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # autoheader: warning: missing template: CUPS_DEFAULT_ACCESS_LOG_LEVEL
        # autoheader: warning: Use AC_DEFINE([CUPS_DEFAULT_ACCESS_LOG_LEVEL], [], [Description])
        # autoheader: warning: missing template: HAVE_ABS
        # autoheader: warning: missing template: HAVE_MALLINFO
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += [
            "--with-cupsd-file-perm=0755",
            "--with-exe-file-perm=755",
            "--with-log-file-perm=0640",
        ]
        self.subinfo.options.install.args = ["install-headers", "install-libs"]

    def install(self):
        if not super().install():
            return False
        return utils.copyFile(self.buildDir() / "cups-config", self.imageDir() / "bin/cups-config")
