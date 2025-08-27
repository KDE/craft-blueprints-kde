# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.CL

    def setTargets(self):
        for ver in ["3.0.0"]:
            self.targets[ver] = f"https://sourceforge.net/projects/pthreads4w/files/pthreads4w-code-v{ver}.zip"

        self.targetDigests["3.0.0"] = (["b81136effb7185c77601fe2e0e6ac19bd996912e4814cebdd3010b0fac9e259b"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["3.0.0"] = "pthreads4w-code-07053a521b0a9deb6db2a649cde1f828f2eb1f4f"

        self.svnTargets["master"] = "https://git.code.sf.net/p/pthreads4w/code"
        self.patchToApply["master"] = [("pthreads-20240811.patch", 1)]

        # The latest release version 3.0.0 does not have CMake support yet, it is only in master
        self.svnTargets["8e467a6"] = "https://git.code.sf.net/p/pthreads4w/code||8e467a62a14fd9de15af33beec0a913d23f4d2f9"
        self.patchToApply["8e467a6"] = [("pthreads-20240811.patch", 1)]

        self.patchLevel["8e467a6"] = 2

        self.description = "A POSIX thread implementation for windows"
        self.defaultTarget = "8e467a6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        # See https://github.com/microsoft/vcpkg/blob/13a0b7ba8dd2af538fdf24d860e67c5b951788fb/ports/pthreads/portfile.cmake#L59
        if not utils.copyFile(self.blueprintDir() / "PThreads4WConfig.cmake", self.imageDir() / "share/PThreads4W/PThreads4WConfig.cmake"):
            return False
        return True
