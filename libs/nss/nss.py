import os
import shutil

import info
from CraftCompiler import CraftCompiler
from Package.MakeFilePackageBase import *
from shells import BashShell

nss_ver = "3.93"
nspr_ver = "4.35"


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = (
            CraftCore.compiler.Platforms.Windows if CraftCore.compiler.isMSVC() else (CraftCore.compiler.Platforms.Linux | CraftCore.compiler.Platforms.Android)
        )
        self.options.dynamic.registerOption("installTools", False)

    def setTargets(self):
        self.description = "Network Security Services (NSS) is a set of libraries designed to support cross-platform development of security-enabled client and server applications."

        # always try to use latest nss with all security fixes
        ver = nss_ver
        self.targets[ver] = f"https://ftp.mozilla.org/pub/security/nss/releases/NSS_3_93_RTM/src/nss-{ver}-with-nspr-{nspr_ver}.tar.gz"
        self.targetInstSrc[ver] = f"nss-{ver}"
        self.targetDigests[ver] = (["4a5b5df21f8accc65b80d38b6acf8b017a5d03b5f81f0d23295a11575f300183"], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isMSVC():
            self.patchToApply[ver] = [("install-instead-of-nsinstall.diff", 1), ("cygwin-is-windows.diff", 1)]
        self.defaultTarget = ver

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["python-modules/gyp-next"] = None


class Package(MakeFilePackageBase):
    def __init__(self):
        MakeFilePackageBase.__init__(self)

    @property
    def makeProgram(self):
        if CraftCore.compiler.isWindows:
            return "make"
        else:
            return super().makeProgram

    def make(self):
        self.enterBuildDir()

        self._shell = BashShell()
        self._shell.environment["MAKE"] = self.makeProgram

        buildArgs = ["-v", "--disable-tests", "--opt", "--system-sqlite", "-Dsign_libs=0"]

        if CraftCore.compiler.isMSVC():
            # When you say --system-sqlite it just tries to find it in the path, that doesn't work for MSVC
            configgypi = self.sourceDir() / "nss/coreconf/config.gypi"
            with open(configgypi, "rt") as f:
                content = f.read()

            content = content.replace(
                "'sqlite_libs%': ['-lsqlite3']", "'sqlite_libs%': ['" + str(OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot())) + "/lib/sqlite3.lib']"
            )

            with open(configgypi, "wt") as f:
                f.write(content)

            clPath = CraftCore.cache.findApplication("cl")
            msvcPath = Path(clPath).parent
            while not os.path.isdir(msvcPath / "VC" / "Tools"):
                newPath = Path(msvcPath).parent
                if newPath == msvcPath:
                    print("Could not figure out which is your MSVC install path")
                    return False
                msvcPath = newPath

            msvcVersionPath = msvcPath
            while not Path(msvcVersionPath).name.isnumeric():
                newPath = Path(msvcVersionPath).parent
                if newPath == msvcVersionPath:
                    print("Could not figure out which is your MSVC version number")
                    return False
                msvcVersionPath = newPath

            self._shell.environment["GYP_MSVS_OVERRIDE_PATH"] = str(msvcPath)
            self._shell.environment["GYP_MSVS_VERSION"] = Path(msvcVersionPath).name

        if CraftCore.compiler.isAndroid:
            # Otherwise gyp isn't found
            self._shell.environment["PATH"] += ":~/.local/bin/"
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
                buildArgs += ["--target=x64", "-DOS=android"]
            else:
                buildArgs += ["--target=" + CraftCore.compiler.androidArchitecture, "-DOS=android"]

            # Inspired by craft's own AutoToolsBuildSystem.py
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.arm32:
                androidtarget = "arm-linux-androideabi"
            elif CraftCore.compiler.architecture == CraftCompiler.Architecture.arm64:
                androidtarget = "aarch64-linux-android"
            elif CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_32:
                androidtarget = "i686-linux-android"
            else:
                androidtarget = f"{CraftCore.compiler.androidArchitecture}-linux-android"

            ndkDir = os.environ.get("ANDROID_NDK")
            toolchainDir = ndkDir + "/toolchains/llvm/prebuilt/" + os.environ.get("ANDROID_NDK_HOST")
            # We need the version so we can call the proper clang compiler
            ndkPlatformVersion = os.environ.get("ANDROID_NDK_PLATFORM").replace("android-", "")

            nsprsh = self.sourceDir() / "nss/coreconf/nspr.sh"
            with open(nsprsh, "rt") as f:
                content = f.read()
            # Tell nspr where the ndk, toolchain and platform are
            newParams = (
                "--target="
                + androidtarget
                + " --with-android-ndk="
                + ndkDir
                + " --with-android-toolchain="
                + toolchainDir
                + " --with-android-platform="
                + toolchainDir
                + "/sysroot"
            )
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
                newParams += " --enable-64bit"
            content = content.replace('extra_params=(--prefix="$dist_dir"/$target)', 'extra_params=(--prefix="$dist_dir"/$target ' + newParams + ")")
            with open(nsprsh, "wt") as f:
                f.write(content)

            nsprconf = self.sourceDir() / "nspr/configure"
            with open(nsprconf, "rt") as f:
                content = f.read()
            # Accept stuff like aarch64-unknown-linux-android, arm-unknown-linux-androideabi, etc.
            content = content.replace("-linux*-android*)", "-*linux*-android*)")
            content = content.replace("-linux*-android*|", "-*linux*-android*|")
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.arm32:
                # For some reason the armv7 compilers have a different name than stuff like ar or ranlib so we need to do a different replacement here ...
                # Call the proper clang, gcc is no longer supported
                content = content.replace(
                    'CC="$android_toolchain"/bin/"$android_tool_prefix"-gcc',
                    'CC="$android_toolchain"/bin/armv7a-linux-androideabi' + ndkPlatformVersion + "-clang",
                )
                content = content.replace(
                    'CXX="$android_toolchain"/bin/"$android_tool_prefix"-g++',
                    'CXX="$android_toolchain"/bin/armv7a-linux-androideabi' + ndkPlatformVersion + "-clang++",
                )
            else:
                # Call the proper clang, gcc is no longer supported
                content = content.replace(
                    'CC="$android_toolchain"/bin/"$android_tool_prefix"-gcc',
                    'CC="$android_toolchain"/bin/"$android_tool_prefix"' + ndkPlatformVersion + "-clang",
                )
                content = content.replace(
                    'CXX="$android_toolchain"/bin/"$android_tool_prefix"-g++',
                    'CXX="$android_toolchain"/bin/"$android_tool_prefix"' + ndkPlatformVersion + "-clang++",
                )
            # Remove useless toolchain mangling
            content = content.replace('android_tool_prefix="i686-android-linux"', ":")

            # Adapt to NDK >= r25 having no GCC binutils anymore
            content = content.replace(
                'AR="$android_toolchain"/bin/"$android_tool_prefix"-ar',
                'AR="$android_toolchain"/bin/llvm-ar'
            )
            content = content.replace(
                'RANLIB="$android_toolchain"/bin/"$android_tool_prefix"-ranlib',
                'RANLIB="$android_toolchain"/bin/llvm-ranlib'
            )
            content = content.replace(
                'STRIP="$android_toolchain"/bin/"$android_tool_prefix"-strip',
                'STRIP="$android_toolchain"/bin/llvm-strip'
            )

            # No cpp tool
            content = content.replace('CPP="$android_toolchain"/bin/"$android_tool_prefix"-cpp', "CPP=")
            # Remove -mandroid in CFLAGS/CXXFLAGS/LDFLAGS
            content = content.replace('FLAGS="-mandroid ', 'FLAGS="')
            with open(nsprconf, "wt") as f:
                f.write(content)

        build = Arguments([self.sourceDir() / "nss/build.sh"])
        return self._shell.execute(self.buildDir(), build, buildArgs)

    def install(self):
        if not BuildSystemBase.install(self):
            return False

        if not (
            utils.copyDir(self.sourceDir() / "dist/Release", self.installDir())
            and utils.copyDir(self.sourceDir() / "dist/public", self.installDir() / "include")
        ):
            return False

        if not self.subinfo.options.dynamic.installTools:
            utils.cleanDirectory(self.installDir() / "bin")

        # NSS has a .pc.in file but doesn't do anything with it
        nsspcSource = os.path.join(self.sourceDir(), "nss/pkg/pkg-config/nss.pc.in")
        nsspcDest = os.path.join(self.installDir(), "lib/pkgconfig/nss.pc")
        shutil.copyfile(nsspcSource, nsspcDest)

        with open(nsspcDest, "rt") as f:
            content = f.read()

        content = content.replace("%libdir%", "${prefix}/lib")
        content = content.replace("%prefix%", str(CraftCore.standardDirs.craftRoot()).replace("\\", "/"))
        content = content.replace("%exec_prefix%", "${prefix}")
        content = content.replace("%includedir%", "${prefix}/include/nss")
        content = content.replace("%NSPR_VERSION%", nspr_ver)
        content = content.replace("%NSS_VERSION%", nss_ver)

        with open(nsspcDest, "wt") as f:
            f.write(content)

        return True

    def postInstall(self):
        BuildSystemBase.patchInstallPrefix(
            self, [(self.installDir() / "lib/pkgconfig/nspr.pc")], [os.path.dirname(self.installDir()) + "/work/nss-" + nss_ver + "/dist/Release"]
        )
        if CraftCore.compiler.isMSVC():
            # The nspr libs are created as libnspr4.lib so we need to adapt the pc file
            nsprpc = self.installDir() / "lib/pkgconfig/nspr.pc"
            with open(nsprpc, "rt") as f:
                content = f.read()

            content = content.replace("-lplc4", "-llibplc4")
            content = content.replace("-lplds4", "-llibplds4")
            content = content.replace("-lnspr4", "-llibnspr4")

            with open(nsprpc, "wt") as f:
                f.write(content)

            # Fix the .lib files names (i.e. foo.dll.lib instead of foo.lib)
            for f in os.listdir(self.installDir() / "lib"):
                full_path = os.path.join(self.installDir() / "lib", f)
                if os.path.isfile(full_path):
                    if not full_path.endswith(".dll.lib"):
                        continue

                    new_name = full_path.replace(".dll.lib", ".lib")
                    os.rename(full_path, new_name)

            # Fix the .dll files being in lib instead of bin
            for f in os.listdir(self.installDir() / "lib"):
                full_path = os.path.join(self.installDir() / "lib", f)
                if os.path.isfile(full_path):
                    if not full_path.endswith(".dll"):
                        continue

                    new_name = full_path.replace("\\lib\\", "\\bin\\")
                    os.rename(full_path, new_name)

        return True
