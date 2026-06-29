import os
import shutil
import sys
from pathlib import Path

import info
import utils
from BuildSystem.BuildSystemBase import BuildSystemBase
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.PackageBase import PackageBase
from Packager.TypePackager import TypePackager
from Source.MultiSource import MultiSource
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.4.9"]:
            self.targets[ver] = f"https://aubio.org/pub/aubio-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"aubio-{ver}"
        self.targetDigests["0.4.9"] = (
            [
                "0cb81bb4b15051db3f3f4d160d500af56fdfb237e0a74e3f366f53c2870030aa0a7cee8469a611a9694c36b8866d3d42ffb48241c999de08f3fee43e6d903130"
            ],
            CraftHash.HashAlgorithm.SHA512,
        )
        self.description = "A tool for extracting annotations from audio signals"
        self.webpage = "https://aubio.org/"
        self.defaultTarget = "0.4.9"

    def setDependencies(self):
        self.buildDependencies["dev-utils/waf"] = None
        self.runtimeDependencies["virtual/base"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/libfftwf"] = None
            self.runtimeDependencies["libs/libsamplerate"] = None
            self.runtimeDependencies["libs/libsndfile"] = None


class WafBuildSystem(BuildSystemBase):
    def __init__(self, package):
        super().__init__(package, "waf")
        self.subinfo.options.useShadowBuild = False

    def configure(self):
        return utils.system(self._wafCommand() + ["configure"] + self.configureOptions(), cwd=self.sourceDir())

    def make(self):
        return utils.system(self._wafCommand() + ["build", "--notests"] + self.makeOptions(None).get(), cwd=self.sourceDir())

    def install(self):
        if not self.cleanImage():
            return False
        if not utils.system(self._wafCommand() + ["install", "--notests", f"--destdir={self.installDir()}"], cwd=self.sourceDir()):
            return False
        return self._fixInstallPrefix(self.installPrefix())

    def configureOptions(self, defines=""):
        prefix = CraftStandardDirs.craftRoot()
        args = [
            f"--prefix={prefix}",
            f"--libdir={prefix / 'lib'}",
            "--build-type=release",
            "--disable-jack",
            "--disable-avcodec",
            "--disable-docs",
            "--disable-tests",
        ]
        if CraftCore.compiler.isAndroid:
            args += [
                "--disable-fftw3f",
                "--disable-sndfile",
                "--disable-samplerate",
            ]
        else:
            args += [
                "--enable-fftw3f",
                "--enable-sndfile",
                "--enable-samplerate",
            ]
        if CraftCore.compiler.isMacOS:
            args += ["--disable-fat"]
        if CraftCore.compiler.isAndroid:
            args += ["--with-target-platform=android"]
        elif getattr(CraftCore.compiler, "isIOS", False):
            args += ["--with-target-platform=ios"]
        return args

    def _wafCommand(self):
        return [sys.executable, self._wafPath()]

    def _wafPath(self):
        return str(CraftStandardDirs.craftRoot() / "dev-utils/bin/waf")


class Package(PackageBase, MultiSource, WafBuildSystem, TypePackager):
    def __init__(self, **kwargs):
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        WafBuildSystem.__init__(self, **kwargs)
        TypePackager.__init__(self, **kwargs)

    def unpack(self):
        if not super().unpack():
            return False

        waflib = self.sourceDir() / "waflib"
        if waflib.exists():
            shutil.rmtree(waflib)
        return True

    def configure(self):
        with utils.ScopedEnv(self._buildEnv()):
            return super().configure()

    def make(self):
        with utils.ScopedEnv(self._buildEnv()):
            return super().make()

    def install(self):
        with utils.ScopedEnv(self._buildEnv()):
            return super().install()

    def _buildEnv(self):
        root = Path(CraftStandardDirs.craftRoot())
        pkgConfigPath = os.pathsep.join(
            [
                str(root / "lib/pkgconfig"),
                str(root / "share/pkgconfig"),
                os.environ.get("PKG_CONFIG_PATH", ""),
            ]
        )
        env = {"PKG_CONFIG_PATH": pkgConfigPath}
        if CraftCore.compiler.isUnix:
            env["LD_LIBRARY_PATH"] = str(root / "lib")
        return env
