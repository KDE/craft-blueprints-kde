import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/xapian/xapian.git"
        self.targetInstSrc["master"] = f"xapian-core"
        for ver in ["1.4.5", "1.4.9"]:
            self.targets[ver] = f"http://oligarchy.co.uk/xapian/{ver}/xapian-core-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"xapian-core-{ver}"
        self.targetDigests["1.4.5"] = (["85b5f952de9df925fd13e00f6e82484162fd506d38745613a50b0a2064c6b02b"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.4.9"] = (["cde9c39d014f04c09b59d9c21551db9794c10617dc69ab4c9826352a533df5cc"], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isWindows:
            self.patchToApply["1.4.5"] = [("xapian-core-1.4.5-20180515.diff", 1)]
            self.patchToApply["1.4.9"] = [("xapian-core-1.4.5-20180515.diff", 1)]
        self.description = "Open Source Search Engine library"
        self.webpage = "https://xapian.org/"
        self.defaultTarget = "1.4.9"

    def setDependencies(self):
        self.runtimeDependencies["libs/libxslt"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static"]
        if CraftCore.compiler.isMSVC():
            self.shell.useMSVCCompatEnv = True
            self.subinfo.options.useShadowBuild = False

    def configure(self):
        if self.buildTarget == "master":
            if not self.shell.execute(self.sourceDir(), "perl", "preautoreconf"):
                return False
        return super().configure()

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMSVC():
            return utils.moveFile(self.installDir() / "lib/xapian.lib", self.installDir() / "lib/libxapian.lib")
        return True

    def postInstall(self):
        return self.patchInstallPrefix(
            [os.path.join(self.installDir(), "lib", "cmake", "xapian", "xapian-config.cmake")],
            OsUtils.toMSysPath(self.subinfo.buildPrefix),
            OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()),
        ) and self.patchInstallPrefix(
            [os.path.join(self.installDir(), "bin", "xapian-config")],
            OsUtils.toMSysPath(self.subinfo.buildPrefix),
            OsUtils.toMSysPath(CraftCore.standardDirs.craftRoot()),
        )
