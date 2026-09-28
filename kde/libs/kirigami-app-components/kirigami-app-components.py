# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Manuel Alcaraz Zambrano <manuel@alcarazzam.dev>

import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Kirigami addons and modules necessary to do a full featured KDE application"

        self.svnTargets["master"] = "https://invent.kde.org/libraries/kirigami-app-components.git"

        for ver in ["1.0.2"]:
            self.targets[ver] = f"https://download.kde.org/stable/kirigami-app-components/kirigami-app-components-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/kirigami-app-components/kirigami-app-components-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = "kirigami-app-components-" + ver

        self.patchToApply["1.0.2"] = [
            ("c3ccb35f56d825b3526468d1e6a1a9e59fbe82fb.patch", 1),  # Install translations
            ("e41e5aacd7bec256eee83e4e1eedf81715bf5508.patch", 1),  # Shortcuts fix
            ("372232c7662fdb0bbfa35f8e805c9f692d768c8a.patch", 1),  # Fix tranlations domain
        ]

        self.defaultTarget = "1.0.2"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None

        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None

        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
