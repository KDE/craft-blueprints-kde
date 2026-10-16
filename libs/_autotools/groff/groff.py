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
        for ver in ["1.23.0", "1.24.2"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/groff/groff-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"groff-{ver}"
        self.targetDigests["1.23.0"] = (["6b9757f592b7518b4902eb6af7e54570bdccba37a871fddb2d30ae3863511c13"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.24.2"] = (["f9c1efd5bebbe37fc6e1063db7473ce8df1e3e0be4ff0f43ce04fce57e9c5dd9"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.24.2"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Upstream still uses K&R function definitions, which do not compile as C23.
        # https://github.com/Homebrew/homebrew-core/blob/9eacf07ea0b69e968deacd2a8080cb320a587c37/Formula/g/groff.rb#L43C4-L43C81
        self.subinfo.options.configure.args += ["ac_cv_prog_cc_c23=no"]
        if not CraftCore.compiler.platform.isLinux:
            self.subinfo.options.configure.args += ["--without-x"]
        # contains host tools with a potentially different architecture, which Craft can't strip
        if CraftCore.compiler.platform.isAndroid:
            self.subinfo.options.package.disableStriping = True
