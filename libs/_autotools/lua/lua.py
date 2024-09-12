import os

import info
import utils
from CraftCore import CraftCore
from Package.MakeFilePackageBase import MakeFilePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "lua"
        self.description = "Lua is a powerful, efficient, lightweight, embeddable scripting language."
        self.defaultTarget = "5.2.4"

        for ver in ["5.2.4"]:
            self.targets[ver] = f"https://www.lua.org/ftp/lua-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"lua-{ver}"
            self.archiveNames[ver] = f"lua-{ver}.tar.gz"

        self.targetDigests["5.2.4"] = (["b9e2e4aad6789b3b63a056d442f7b39f0ecfca3ae0f1fc0ae4e9614401b69f4b"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["5.2.4"] = [("0002-generate-pc-file.patch", 1)]
        if CraftCore.compiler.isUnix:
            self.patchToApply["5.2.4"] += [("0001-build-shared-library.patch", 1)]
        self.patchLevel["5.2.4"] = 3

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(MakeFilePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.make.supportsMultijob = not CraftCore.compiler.isWindows
        if CraftCore.compiler.isUnix:
            self.subinfo.options.make.args += ["generic"]
        if CraftCore.compiler.isWindows:
            self.subinfo.options.make.args += ["mingw"]
        self.subinfo.options.make.args += ["lua5.2.pc"]

    def install(self):
        self.enterSourceDir()

        includeDir = self.installDir() / "include/lua/lua5.2"
        if CraftCore.compiler.isWindows:
            includeDir = self.installDir() / "include"

        files = [
            ("lua5.2.pc", self.installDir() / "lib/pkgconfig/lua5.2.pc"),
            ("lua5.2.pc", self.installDir() / "lib/pkgconfig/lua.pc"),
            ("src/liblua.so.5.2.4", self.installDir() / "lib/liblua.so.5.2.4"),
            ("src/lua", self.installDir() / "bin/lua"),
            ("src/luac", self.installDir() / "bin/luac"),
            ("src/liblua.a", self.installDir() / "lib/liblua.a"),
            ("src/lua52.dll", self.installDir() / "bin/lua52.dll"),
            ("src/lua.exe", self.installDir() / "bin/lua.exe"),
            ("src/luac.exe", self.installDir() / "bin/luac.exe"),
            ("src/lua.h", includeDir / "lua.h"),
            ("src/luaconf.h", includeDir / "luaconf.h"),
            ("src/lualib.h", includeDir / "lualib.h"),
            ("src/lauxlib.h", includeDir / "lauxlib.h"),
            ("src/lua.hpp", includeDir / "lua.hpp"),
            ("doc/lua.1", self.installDir() / "man/man1/lua.1"),
            ("doc/luac.1", self.installDir() / "man/man1/luac.1"),
        ]
        # install files
        for src, dest in files:
            source = self.workDir() / "lua-5.2.4" / src
            if os.path.exists(source):
                CraftCore.log.info(f"Installing {source} -> {dest}")
                if not utils.copyFile(source, dest):
                    return False

        if CraftCore.compiler.isUnix:
            liblua = self.installDir() / "lib/liblua.so.5.2.4"
            if os.path.exists(liblua):
                if (
                    not utils.createSymlink(liblua, self.installDir() / "lib/liblua.so.5.2")
                    or not utils.createSymlink(liblua, self.installDir() / "lib/liblua.so.5")
                    or not utils.createSymlink(liblua, self.installDir() / "lib/liblua.so.0")
                    or not utils.createSymlink(liblua, self.installDir() / "lib/liblua.so")
                ):
                    return False

        return True
