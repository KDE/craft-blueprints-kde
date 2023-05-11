# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2022 Hannah von Reth <vonreth@kde.org>
import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.defaultTarget = "latest"

    def setDependencies(self):
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.buildDependencies[f"libs/qt6/{self.parent.package.name}"] = None
        else:
            self.buildDependencies[f"libs/qt5/{self.parent.package.name}"] = None


class Package(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)
