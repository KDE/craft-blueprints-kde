# SPDX-FileCopyrightText: 2023 G10 Code
# SPDX-FileContributor: Carl Schwan <carl.schwan@gnupg.com>
# SPDX-License-Identifier: BSD-2-Clause

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.3.2"]:
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/ntbtls/ntbtls-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"ntbtls-{ver}"
            self.patchToApply[ver] = ("install-ntbtls.diff", 1)
        self.targetDigests["0.3.2"] = (["bdfcb99024acec9c6c4b998ad63bb3921df4cfee4a772ad6c0ca324dbbf2b07c"], CraftHash.HashAlgorithm.SHA256)
        self.description = "The Not Too Bad TLS Library"
        self.defaultTarget = "0.3.2"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/libksba"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared"]
