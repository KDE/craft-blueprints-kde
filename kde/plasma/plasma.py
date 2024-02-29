# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>
from Blueprints.CraftPackageObject import CraftPackageObject


class Pattern(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            self.subinfo.defaultTarget = "5.27.10"
