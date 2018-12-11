import tempfile

import info
from Package.AutoToolsPackageBase import *
from Package.MakeFilePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["5.28.1"]:
            self.targets[ver] = f"https://www.cpan.org/src/5.0/perl-{ver}.tar.gz"
            self.targetInstallPath[ver] = os.path.join("dev-utils", "perl")
            if CraftCore.compiler.isWindows:
                self.targetInstSrc[ver] = f"perl-{ver}/win32"
            else:
                self.targetInstSrc[ver] = f"perl-{ver}"

        if CraftCore.compiler.isWindows:
            # With msvc2015+ and Windows 10 1803 perlglob is broken. for that reason we provide a precompiled version
            # https://developercommunity.visualstudio.com/content/problem/245615/first-file-name-in-command-line-wildcard-expansion.html
            self.patchToApply["5.28.0"] = [("perl-5.28.0-20181129.diff", 1)]
            self.patchToApply["5.28.1"] = [("perl-5.28.0-20181129.diff", 1)]
        self.targetDigests["5.28.0"] = (['7e929f64d4cb0e9d1159d4a59fc89394e27fa1f7004d0836ca0d514685406ea8'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["5.28.0"] = (['3ebf85fe65df2ee165b22596540b7d5d42f84d4b72d84834f74e2e0b8956c347'],CraftHash.HashAlgorithm.SHA256)
        self.description = ("Perl 5 is a highly capable, feature-rich programming language with over 30 years of "
                            "development. Perl 5 runs on over 100 platforms from portables to mainframes and is "
                            "suitable for both rapid prototyping and large scale development projects.")
        self.patchLevel["5.28.0"] = 5
        self.defaultTarget = "5.28.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def _installExtraModules(self, package):
        # we need a fresh config
        with tempfile.TemporaryDirectory() as tmp:
            with utils.ScopedEnv({"HOME": tmp, "USERPROFILE": tmp}):
                perl = os.path.join(package.installDir(), "bin", "perl")
                if CraftCore.compiler.isWindows:
                    if not utils.system([f"cmd", "/C", f"echo yes | {perl} -MCPAN -e mkmyconfig"], shell=True):
                        return False
                else:
                    if not utils.system([f"yes | {perl} -MCPAN -e mkmyconfig"], shell=True):
                        return False

                for module in ["URI::URL"]:
                    if not utils.system([perl, "-MCPAN",  "-e", f"CPAN::Shell->notest('force', 'install', '{module}')"]):
                        return False
            # we might need to force the deletion
            OsUtils.rmDir(tmp, True)
            # tmp file expects this dir to exist..
            utils.createDir(tmp)
        return True


class PackageMSVC(MakeFilePackageBase):
    def __init__(self, **args):
        MakeFilePackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.useShadowBuild = False
        config = {  "CCTYPE": "MSVC141" if CraftCore.compiler.isMSVC() else "GCC",
                    "CRAFT_DESTDIR": self.installDir(),
                    "CRAFT_WIN64": "" if CraftCore.compiler.isX64() else "undef",
                    "PLMAKE": "nmake" if CraftCore.compiler.isMSVC() else "mingw32-make"}

        if CraftCore.compiler.isMinGW():
            config["CCHOME"] = os.path.join(CraftCore.standardDirs.craftRoot(), "mingw64")
            config["SHELL"] = os.environ["COMSPEC"]
        elif CraftCore.compiler.isX86():
            config["PROCESSOR_ARCHITECTURE"] = CraftCore.compiler.architecture


        self.subinfo.options.make.args += " ".join(["{0}={1}".format(x, y) for x, y in config.items()])
        self.subinfo.options.install.args = f"{self.subinfo.options.make.args} installbare"


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
            return (super().install() and
                    utils.globCopyDir(os.path.join(self.sourceDir(), ".."), os.path.join(self.installDir(), "lib"),
                                      ["perl5*.lib", "perl5*.pdb"]) and
                    utils.globCopyDir(os.path.join(self.sourceDir(), "..", "lib", "CORE"),
                                      os.path.join(self.installDir(), "include", "perl"), ["**/*.h"]) and
                    self.subinfo._installExtraModules(self))

    def postInstall(self):
        newPrefix = OsUtils.toUnixPath(self.installPrefix())
        oldPrefixes = [self.installDir(), OsUtils.toUnixPath(self.installDir())]

        pattern = [re.compile("^.*(pl)$")]
        files = utils.filterDirectoryContent(self.installDir(),
                                             whitelist=lambda x, root: utils.regexFileFilter(x, root, pattern),
                                             blacklist=lambda x, root: True)

        if not self.patchInstallPrefix(files, oldPrefixes, newPrefix):
            return False
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "perl.exe"),
                                os.path.join( self.installDir(), "bin", "perl.exe"))


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        # https://metacpan.org/pod/distribution/perl/INSTALL
        self.subinfo.options.install.args = "install.perl"
        self.subinfo.options.configure.args = f"-des -D 'prefix={self.installPrefix()}' -D mksymlinks  -D userelocatableinc -U default_inc_excludes_dot"

        cflags = self.shell.environment["CFLAGS"]
        ldflags = self.shell.environment["LDFLAGS"]
        if CraftCore.compiler.isGCC() and not CraftCore.compiler.isNative() and CraftCore.compiler.isX86():
            cflags += " -m32"
            ldflags += " -m32"
            self.subinfo.options.configure.args += " -Alddlflags='-m32 -shared' -Uuse64bitint -Uuse64bitall"
        self.subinfo.options.configure.args += f" -Accflags='{cflags}' -Aldflags='{ldflags}' "

    def configure(self):
        self.enterBuildDir()
        return self.shell.execute(self.buildDir(), os.path.join(self.sourceDir(), "Configure"),
                                  self.subinfo.options.configure.args)


    def install(self):
        return super().install() and self.subinfo._installExtraModules(self)

    def postInstall(self):
        return utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "perl"),
                                os.path.join( self.installDir(), "bin", "perl"))


if CraftCore.compiler.isUnix:
    class Package(PackageAutoTools):
        pass
else:
    class Package(PackageMSVC):
        pass
