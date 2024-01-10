import info
from CraftOS.osutils import OsUtils
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Tom's LADSPA Plugins"
        self.webpage = "https://tomscii.sig7.se/tap-plugins/"

        # for ver in ["1.0.1"]:
        #     self.targets[ver] = f"https://github.com/tomszilagyi/tap-plugins/archive/v{ver}.tar.gz"
        #     self.targetInstSrc[ver] = f"tap-plugins-{ver}"
        #     self.patchToApply[ver] = ("tap-mingw.patch", 0)
        # self.targetDigests["1.0.1"] = (["89c932bea903589db2717ca4d87013fea404b4123fc71acba5bc7cba18d3ecbb"], CraftHash.HashAlgorithm.SHA256)

        # The project was removed from GitHub. There is a blog post about this that announcences, tar.gz files will still be available
        # but I could not find them so maybe this will be added back later and we can use them again
        # See https://tomscii.sig7.se/2024/01/Ditching-GitHub
        self.svnTargets["8564022"] = "https://git.hq.sig7.se/tap-plugins.git||85640223047d49a305e90ba1b92303eb066ba474"
        self.patchToApply["8564022"] = ("tap-mingw.patch", 0)

        self.defaultTarget = "8564022"

    def setDependencies(self):
        self.buildDependencies["libs/ladspa-sdk"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.useShadowBuild = False
        inst = OsUtils.toMSysPath(self.installDir())
        self.subinfo.options.install.args += [f"INSTALL_PLUGINS_DIR={inst}/lib/ladspa/", f"INSTALL_LRDF_DIR={inst}/share/ladspa/rdf/"]

    def configure(self):
        return True
