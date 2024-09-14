# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Common high-level interface to speech synthesis"

        for ver in ["0.11.5"]:
            self.targets[ver] = f"https://github.com/brailcom/speechd/releases/download/{ver}/speech-dispatcher-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"speech-dispatcher-{ver}"
        self.targetDigests["0.11.5"] = (["1ce4759ffabbaf1aeb433a5ec0739be0676e9bdfbae9444a7b3be1b2af3ec12b"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["0.11.5"] = [("disable-help2man.diff", 1)]

        self.svnTargets["master"] = "https://github.com/brailcom/speechd.git"
        self.patchLevel["master"] = 20220321

        self.defaultTarget = "0.11.5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/libtool"] = None  # For ltdl
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/dotconf"] = None
        self.runtimeDependencies["libs/libsndfile"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.ldflags += " -lintl"
