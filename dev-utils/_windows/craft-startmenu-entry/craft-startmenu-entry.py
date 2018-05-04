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
        self.targets["2"] = f""
        self.defaultTarget = "2"


from Package.BinaryPackageBase import *


class WinPackage(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True
        self._shortcutPath = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Craft", f"Craft {os.path.basename(CraftCore.standardDirs.craftRoot())}.lnk")

    def postQmerge(self):
        powershell = CraftCore.cache.findApplication("powershell")
        root = OsUtils.toNativePath(os.path.join(CraftCore.standardDirs.craftBin(), ".."))
        utils.system([powershell,
                      "-NoProfile",
                      "-ExecutionPolicy", "ByPass",
                      "-Command",
                      os.path.join(self.packageDir(), "install-lnk.ps1"),
                      "-Path", f"'{powershell}'",
                      "-Arguments", "'-NoExit -ExecutionPolicy ByPass -Command .\craftenv.ps1'",
                      "-WorkingDirectory", f"'{root}'",
                      "-Name", f"'{self._shortcutPath}'",
                      "-Icon", "'{0}'".format(os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craft.ico")),
                      "-Description", f"'Craft installed to: {os.path.dirname(root)}'"])
        return True

    def unmerge(self):
        if os.path.exists(self._shortcutPath):
            utils.deleteFile(self._shortcutPath)
        return super().unmerge()

from Package.MaybeVirtualPackageBase import *

class Package(MaybeVirtualPackageBase):
    def __init__(self):
        MaybeVirtualPackageBase.__init__(self, OsUtils.isWin(), classA=WinPackage)
