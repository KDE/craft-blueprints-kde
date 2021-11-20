import tempfile

import CraftOS
import info
from Package.AutoToolsPackageBase import *
from Package.MakeFilePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["5.28.1"]:
            self.targets[ver] = f"https://www.cpan.org/src/5.0/perl-{ver}.tar.gz"
            if CraftCore.compiler.isWindows:
                self.targetInstSrc[ver] = f"perl-{ver}/win32"
            else:
                self.targetInstSrc[ver] = f"perl-{ver}"

        if CraftCore.compiler.isWindows:
            # With msvc2015+ and Windows 10 1803 perlglob is broken. for that reason we provide a precompiled version
            # https://developercommunity.visualstudio.com/content/problem/245615/first-file-name-in-command-line-wildcard-expansion.html
            self.patchToApply["5.28.1"] = [("perl-5.28.0-20181129.diff", 1),
                                           ("perl-5.28.1-20181229.diff", 2)
                                           ]
        else:
            #https://github.com/Perl/perl5/pull/17946/files
            self.patchToApply["5.28.1"] = [("17946.diff", 1)]
        self.targetDigests["5.28.1"] = (['3ebf85fe65df2ee165b22596540b7d5d42f84d4b72d84834f74e2e0b8956c347'],CraftHash.HashAlgorithm.SHA256)
        self.description = ("Perl 5 is a highly capable, feature-rich programming language with over 30 years of "
                            "development. Perl 5 runs on over 100 platforms from portables to mainframes and is "
                            "suitable for both rapid prototyping and large scale development projects.")
        self.patchLevel["5.28.1"] = 6
        self.defaultTarget = "5.28.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class PackageMSVC(MakeFilePackageBase):
    def __init__(self, **args):
        MakeFilePackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.useShadowBuild = False

        root = OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())
        config = {  "CCTYPE": "MSVC141" if CraftCore.compiler.isMSVC() else "GCC",
                    "CRAFT_DESTDIR": self.installDir(),
                    "CRAFT_WIN64": "" if CraftCore.compiler.isX64() else "undef",
                    "PLMAKE": "nmake" if CraftCore.compiler.isMSVC() else "mingw32-make"}

        if CraftCore.compiler.isMinGW():
            config["CCHOME"] = os.path.join(CraftCore.standardDirs.craftRoot(), "mingw64")
            config["SHELL"] = os.environ["COMSPEC"]
            config["CRAFT_CFLAGS"] = f"{os.environ.get('CFLAGS', '')} -I'{root}/include' -L'{root}/lib'"
        elif CraftCore.compiler.isX86():
            config["PROCESSOR_ARCHITECTURE"] = CraftCore.compiler.architecture


        self.subinfo.options.make.args += ["{0}={1}".format(x, y) for x, y in config.items()]
        self.subinfo.options.install.args += self.subinfo.options.make.args + ["installbare"]


    def _globEnv(self):
        env = {}
        if CraftCore.compiler.isMSVC():
            env = {"PATH": f"{self.packageDir()};{os.environ['PATH']}"}
        return env

    def make(self):
        with utils.ScopedEnv(self._globEnv()):
            return super().make()

    def install(self):
        with utils.ScopedEnv(self._globEnv()):
            if not super().install():
                return False
        def makeWriatable(root):
            with os.scandir(root) as scan:
                for f in scan:
                    utils.makeWritable(f.path)
                    if f.is_dir():
                        makeWriatable(f.path)
        makeWriatable(self.installDir())
        return True

    def postInstall(self):
        # in difference to the defaultePrefix replace, we replace the installDir with the installPrefix
        # not an older install prefix with another
        newPrefix = OsUtils.toUnixPath(self.installPrefix())
        oldPrefixes = [self.installDir()]
        files = utils.filterDirectoryContent(self.installDir(),
                                             whitelist=lambda x, root: Path(x).suffix in BuildSystemBase.PatchableFile,
                                             blacklist=lambda x, root: True)
        return self.patchInstallPrefix(files, oldPrefixes, newPrefix)


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        # https://metacpan.org/pod/distribution/perl/INSTALL
        self.subinfo.options.install.args = Arguments(["install.perl"])
        self.subinfo.options.configure.args = Arguments(["-des",
            "-D", f"prefix={self.installPrefix()}",
            "-D", "mksymlinks",
            "-D", "userelocatableinc",
            "-U", "default_inc_excludes_dot",
            "-D", "usethreads"])

        if CraftCore.compiler.isFreeBSD:
            self.subinfo.options.make.supportsMultijob = False

        cflags = self.shell.environment["CFLAGS"]
        ldflags = self.shell.environment["LDFLAGS"]
        if CraftCore.compiler.isGCC() and not CraftCore.compiler.isNative() and CraftCore.compiler.isX86():
            cflags += " -m32"
            ldflags += " -m32"
            self.subinfo.options.configure.args += ["-Alddlflags=-m32 -shared", "-Uuse64bitint -Uuse64bitall"]
        self.subinfo.options.configure.args += ["-A", f"ccflags={cflags}", "-A", f"ldflags={ldflags}"]

    def configure(self):
        self.enterBuildDir()
        return self.shell.execute(self.buildDir(), self.sourceDir() / "Configure",
                                  self.subinfo.options.configure.args)

    def install(self):
        if not super().install():
            return False
        def makeWriatable(root):
            with os.scandir(root) as scan:
                for f in scan:
                    utils.makeWritable(f.path)
                    if f.is_dir():
                        makeWriatable(f.path)
        makeWriatable(self.installDir())
        return True

    def postInstall(self):
        hardCoded = [os.path.join(self.imageDir(), x) for x in ["bin/pod2man"]]
        return self.patchInstallPrefix(hardCoded, self.subinfo.buildPrefix, CraftCore.standardDirs.craftRoot())




if CraftCore.compiler.isUnix:
    class Package(PackageAutoTools):
        pass
else:
    class Package(PackageMSVC):
        pass
