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
        self.options.dynamic.registerOption("usePowershellCore", True)

    def setDependencies(self):
        self.buildDependencies["dev-utils/kshimgen"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True

    @property
    def powershell(self):
        pwsh = None
        # prefer pwsh if installed
        if self.subinfo.options.dynamic.usePowershellCore:
            pwsh = CraftCore.cache.findApplication("pwsh")
        return pwsh or CraftCore.cache.findApplication("powershell")

    @property
    def windowsTerminal(self):
        wt = Path(os.environ["APPDATA"]).parent / "Local/Microsoft/WindowsApps/wt.exe"
        # its a symlink/junction path.exists() crashes
        if os.path.lexists(wt):
            return wt
        return None

    def install(self):
        command = ["-NoExit", "-ExecutionPolicy", "ByPass", "-Command", Path(CraftCore.standardDirs.craftBin()).parent / "craftenv.ps1"]
        out = Path(self.installDir()) / "bin/craftenv.exe"
        wt = self.windowsTerminal
        # Windows allows only one shortcut to the same exe in one dir -> so use a shim
        if not wt:
            return utils.createShim(out, self.powershell, command, useAbsolutePath=True)
        else:
            return utils.createShim(out, wt, ["new-tab", self.powershell] + command, useAbsolutePath=True, guiApp=True)

    def postQmerge(self):
        utils.installShortcut(
            f"Craft {Path(CraftCore.standardDirs.craftRoot()).name}",
            Path(CraftCore.standardDirs.craftRoot()) / "bin/craftenv.exe",
            Path(CraftCore.standardDirs.craftBin()).parent,
            Path(CraftCore.standardDirs.craftBin()) / "data/icons/craft.ico",
            f"Craft installed to: {Path(CraftCore.standardDirs.craftRoot()).name}",
        )
        return True

    def unmerge(self, dbOnly=False):
        shortcutPath = Path(os.environ["APPDATA"]) / f"Microsoft/Windows/Start Menu/Programs/Craft/Craft {Path(CraftCore.standardDirs.craftRoot()).name}.lnk"
        if os.path.exists(shortcutPath):
            utils.deleteFile(shortcutPath)
        return super().unmerge(dbOnly)
