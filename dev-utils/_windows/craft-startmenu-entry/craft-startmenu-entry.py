# -*- coding: utf-8 -*-
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.


import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["3"] = ""
        self.defaultTarget = "3"

    def registerOptions(self):
        self.options.dynamic.registerOption("usePowershellCore", False)

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None

from Package.BinaryPackageBase import *


class WinPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True


    @property
    def powershell(self):
        if not self.subinfo.options.dynamic.usePowershellCore:
            return CraftCore.cache.findApplication("powershell")
        else:
            return CraftCore.cache.findApplication("pwsh")

    def install(self):
        return utils.createShim(os.path.join(self.installDir(), "bin", "craftenv.exe"),
                                self.powershell,
                                ["-NoExit", "-ExecutionPolicy", "ByPass", "-Command", os.path.join(CraftCore.standardDirs.craftBin(), "..", "craftenv.ps1")],
                                useAbsolutePath=True)

    def postQmerge(self):
        utils.installShortcut(f"Craft {os.path.basename(CraftCore.standardDirs.craftRoot())}",
                              os.path.join(CraftCore.standardDirs.craftRoot(), "bin", "craftenv.exe"),
                              os.path.join(CraftCore.standardDirs.craftBin(), ".."),
                              os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craft.ico"),
                              f"Craft installed to: {os.path.dirname(CraftCore.standardDirs.craftRoot())}")
        return True

    def unmerge(self):
        shortcutPath = Path(os.environ["APPDATA"]) / f"Microsoft/Windows/Start Menu/Programs/Craft/Craft {os.path.basename(CraftCore.standardDirs.craftRoot())}.lnk"
        if os.path.exists(shortcutPath):
            utils.deleteFile(shortcutPath)
        return super().unmerge()

from Package.MaybeVirtualPackageBase import *

class Package(MaybeVirtualPackageBase):
    def __init__(self):
        MaybeVirtualPackageBase.__init__(self, OsUtils.isWin(), classA=WinPackage)
