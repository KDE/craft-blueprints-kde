import os
import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.displayName = "lua"
        self.description = "Lua is a powerful, efficient, lightweight, embeddable scripting language."
        self.defaultTarget = "5.2.4"

        for ver in ["5.2.4"]:
            self.targets[ver] = f"https://www.lua.org/ftp/lua-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"lua-{ver}"
            self.archiveNames[ver] = f"lua-{ver}.tar.gz"

        self.targetDigests["5.2.4"] = (["b9e2e4aad6789b3b63a056d442f7b39f0ecfca3ae0f1fc0ae4e9614401b69f4b"], CraftHash.HashAlgorithm.SHA256)
        if OsUtils.isUnix() :
            self.patchToApply["5.2.4"] = [("0001-build-shared-library.patch", 1)]
            self.patchToApply["5.2.4"] += [("0002-generate-pc-file.patch", 1)]


    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = None

from Package.MakeFilePackageBase import *

class Package( MakeFilePackageBase ):
    def __init__(self):
        MakeFilePackageBase.__init__(self)
        if OsUtils.isUnix() :
            self.subinfo.options.make.args += ["-C", f"{self.workDir()}/lua-5.2.4", "generic"]
        if OsUtils.isWin() :
            self.subinfo.options.make.args += ["-C", f"{self.workDir()}/lua-5.2.4", "mingw"]

    def install(self):
        if OsUtils.isUnix() :
            # generate and install lua5.2.pc file
            os.chdir(os.path.join(self.workDir(), "lua-5.2.4"))
            os.system("make lua5.2.pc")
            utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "lua5.2.pc"),
                           os.path.join(self.installDir(), "lib", "pkgconfig", "lua5.2.pc"))

            # install libraries
            liblua = os.path.join(self.installDir(), "lib", "lua", "lua5.2", "liblua.so.5.2.4")
            utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "liblua.so.5.2.4"), liblua)
            utils.createSymlink(liblua, os.path.join(self.installDir(), "lib", "lua", "lua5.2", "liblua.so"))
            utils.createSymlink(liblua, os.path.join(self.installDir(), "lib", "lua", "lua5.2", "liblua.so.5.2"))
            utils.createSymlink(liblua, os.path.join(self.installDir(), "lib", "lua", "lua5.2", "liblua5.2.so"))
            utils.createSymlink(liblua, os.path.join(self.installDir(), "lib", "lua", "lua5.2", "liblua5.2.4.so"))

            # install executables
            utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "lua"),
                           os.path.join(self.installDir(), "bin", "lua"))
            utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "luac"),
                           os.path.join(self.installDir(), "bin", "luac"))

        if OsUtils.isWin() :
            utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "liblua.a"),
                           os.path.join(self.installDir(), "bin", "liblua.a"))
            utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "lua52.dll"),
                           os.path.join(self.installDir(), "bin", "lua52.dll"))

            utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "lua.exe"),
                           os.path.join(self.installDir(), "bin", "lua.exe"))

            utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "luac.exe"),
                           os.path.join(self.installDir(), "bin", "luac.exe"))

        # install headers
        includeDir = os.path.join(self.installDir(), "include", "lua", "lua5.2")
        if OsUtils.isWin() :
            includeDir = os.path.join(self.installDir(), "include")

        utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "lua.h"),
                       os.path.join(includeDir, "lua.h"))

        utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "luaconf.h"),
                       os.path.join(includeDir, "luaconf.h"))

        utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "lualib.h"),
                       os.path.join(includeDir, "lualib.h"))

        utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "lauxlib.h"),
                      os.path.join(includeDir, "lauxlib.h"))

        utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "src", "lua.hpp"),
                      os.path.join(includeDir, "lua.hpp"))

        # install docs
        utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "doc", "lua.1"),
                       os.path.join(self.installDir(), "man", "man1", "lua.1"))

        utils.copyFile(os.path.join(self.workDir(), "lua-5.2.4", "doc", "luac.1"),
                       os.path.join(self.installDir(), "man", "man1", "luac.1"))

        return True
