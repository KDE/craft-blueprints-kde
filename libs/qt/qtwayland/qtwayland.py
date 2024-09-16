# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2022 Hannah von Reth <vonreth@kde.org>
import info
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.runtimeDependencies[f"libs/qt6/{self.parent.package.name}"] = None


class Package(VirtualPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
