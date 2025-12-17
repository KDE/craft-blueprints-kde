import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Syntax highlighting engine for Kate syntax definitions."
        self.displayName = "KSyntaxHighlighting"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def make(self):
        if CraftCore.compiler.isAndroid:
            # this does build a host tool, which fails if we force the compiler to the one of the target
            # not setting CC/CXX OTOH is fine, it'll find everything it needs for the target in the CMake toolchain file
            env = {}
            env["CC"] = None
            env["CXX"] = None
            with utils.ScopedEnv(env):
                return super().make()
        else:
            return super().make()
