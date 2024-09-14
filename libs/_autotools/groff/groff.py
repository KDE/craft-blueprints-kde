# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.description = "GNU roff is a typesetting system that reads plain text input files that include formatting commands to produce output in PostScript, PDF, HTML, or DVI formats or for display to a terminal."
        for ver in ["1.23.0"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/groff/groff-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"groff-{ver}"
        self.targetDigests["1.23.0"] = (["6b9757f592b7518b4902eb6af7e54570bdccba37a871fddb2d30ae3863511c13"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.23.0"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # contains host tools with a potentially different architecture, which Craft can't strip
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.package.disableStriping = True
