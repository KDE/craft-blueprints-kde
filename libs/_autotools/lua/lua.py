import os

import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


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
        if OsUtils.isUnix():
            self.patchToApply["5.2.4"] = [("0001-build-shared-library.patch", 1)]
            self.patchToApply["5.2.4"] += [("0002-generate-pc-file.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.MakeFilePackageBase import *


class Package(MakeFilePackageBase):
    def __init__(self):
        MakeFilePackageBase.__init__(self)
        self.subinfo.options.useShadowBuild = False
        if OsUtils.isUnix():
            self.subinfo.options.make.args += ["generic"]
        if OsUtils.isWin():
            self.subinfo.options.make.args += ["mingw"]

    def install(self):
        self.enterSourceDir()
        if OsUtils.isUnix():
            # generate  lua5.2.pc file
            if not utils.system(["make", "lua5.2.pc"]):
                return False

        includeDir = os.path.join(self.installDir(), "include/lua/lua5.2")
        if OsUtils.isWin():
            includeDir = os.path.join(self.installDir(), "include")

        files = {
            "lua5.2.pc": os.path.join(self.installDir(), "lib/pkgconfig/lua5.2.pc"),
            "lua5.2.pc": os.path.join(self.installDir(), "lib/pkgconfig/lua.pc"),
            "src/liblua.so.5.2.4": os.path.join(self.installDir(), "lib/lua/lua5.2/liblua.so.5.2.4"),
            "src/lua": os.path.join(self.installDir(), "bin/lua"),
            "src/luac": os.path.join(self.installDir(), "bin/luac"),
            "src/liblua.a": os.path.join(self.installDir(), "bin/liblua.a"),
            "src/lua52.dll": os.path.join(self.installDir(), "bin/lua52.dll"),
            "src/lua.exe": os.path.join(self.installDir(), "bin/lua.exe"),
            "src/luac.exe": os.path.join(self.installDir(), "bin/luac.exe"),
            "src/lua.h": os.path.join(includeDir, "lua.h"),
            "src/luaconf.h": os.path.join(includeDir, "luaconf.h"),
            "src/lualib.h": os.path.join(includeDir, "lualib.h"),
            "src/lauxlib.h": os.path.join(includeDir, "lauxlib.h"),
            "src/lua.hpp": os.path.join(includeDir, "lua.hpp"),
            "doc/lua.1": os.path.join(self.installDir(), "man/man1/lua.1"),
            "doc/luac.1": os.path.join(self.installDir(), "man/man1/luac.1"),
        }

        # install files
        for src, dest in files.items():
            source = os.path.join(self.workDir(), "lua-5.2.4", src)
            if os.path.exists(source):
                if not utils.copyFile(source, dest):
                    return False

        if OsUtils.isUnix():
            liblua = os.path.join(self.installDir(), "lib/lua/lua5.2/liblua.so.5.2.4")
            if os.path.exists(liblua):
                if (
                    not utils.createSymlink(liblua, os.path.join(self.installDir(), "lib/lua/lua5.2/liblua.so.5.2"))
                    or not utils.createSymlink(liblua, os.path.join(self.installDir(), "lib/lua/lua5.2/liblua.so.5"))
                    or not utils.createSymlink(liblua, os.path.join(self.installDir(), "lib/lua/lua5.2/liblua.so.0"))
                    or not utils.createSymlink(liblua, os.path.join(self.installDir(), "lib/lua/lua5.2/liblua.so"))
                ):
                    return False

        return True
