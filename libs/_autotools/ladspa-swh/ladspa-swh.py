import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "The SWH Plugins package for the LADSPA plugin system"
        self.webpage = "http://plugin.org.uk/"

        for ver in ["0.4.17"]:
            self.targets[ver] = f"https://github.com/swh/ladspa/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ladspa-{ver}"
        self.targetDigests["0.4.17"] = (["d1b090feec4c5e8f9605334b47faaad72db7cc18fe91d792b9161a9e3b821ce7"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/swh/ladspa.git"
        self.svnTargets["d99a0db"] = "https://github.com/swh/ladspa.git||d99a0db521d13a87bdaa418c674ca8858e484452"
        self.patchToApply["d99a0db"] = ("fix-perl-path.diff", 1)
        self.defaultTarget = "d99a0db"

    def setDependencies(self):
        self.runtimeDependencies["libs/libfftwf"] = None
        self.buildDependencies["libs/gettext"] = None
        self.buildDependencies["libs/ladspa-sdk"] = None
        self.buildDependencies["libs/libxml2"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["perl-modules/list-moreutils"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.make.args += f"PERL5LIB={self.shell.toNativePath(CraftCore.standardDirs.craftRoot())}/lib/perl5/site_perl/5.28.1"
