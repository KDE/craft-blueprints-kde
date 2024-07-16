import os

import info
import utils
from Blueprints.CraftVersion import CraftVersion
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.4", "5.0.1", "6.0", "6.1.1"]:
            self.targets[ver] = f"https://ffmpeg.org/releases/ffmpeg-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"ffmpeg-{ver}"
        self.svnTargets["master"] = "https://git.ffmpeg.org/ffmpeg.git"
        self.targetDigests["4.4"] = (["42093549751b582cf0f338a21a3664f52e0a9fbe0d238d3c992005e493607d0e"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["5.0.1"] = (["28df33d400a1c1c1b20d07a99197809a3b88ef765f5f07dc1ff067fac64c59d6"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["6.0"] = (["47d062731c9f66a78380e35a19aac77cebceccd1c7cc309b9c82343ffc430c3d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["6.1.1"] = (["5e3133939a61ef64ac9b47ffd29a5ea6e337a4023ef0ad972094b4da844e3a20"], CraftHash.HashAlgorithm.SHA256)

        # https://github.com/FFmpeg/FFmpeg/commit/effadce6c756247ea8bae32dc13bb3e6f464f0eb
        # Fix assembling with binutil >= 2.41
        self.patchToApply["6.0"] = [("effadce6c756247ea8bae32dc13bb3e6f464f0eb.diff", 1)]

        if CraftCore.compiler.isMSVC():
            self.patchToApply["4.4"] = [("ffmpeg-4.4-20210413.diff", 1)]
            self.patchToApply["5.0.1"] = [("ffmpeg-4.4-20210413.diff", 1)]
            self.patchToApply["6.0"] += [("ffmpeg-4.4-20210413.diff", 1)]
            self.patchToApply["6.1.1"] = [("ffmpeg-4.4-20210413.diff", 1)]
        else:
            self.patchLevel["4.4"] = 1

        self.patchLevel["5.0.1"] = 4
        self.patchLevel["6.0"] = 3
        self.patchLevel["6.1.1"] = 2

        self.description = "A complete, cross-platform solution to record, convert and stream audio and video."
        self.webpage = "https://ffmpeg.org/"
        self.defaultTarget = "6.1.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblame"] = None
        self.runtimeDependencies["libs/libopus"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/x265"] = None
        self.runtimeDependencies["libs/libvorbis"] = None
        self.runtimeDependencies["libs/libsdl2"] = None
        self.runtimeDependencies["libs/aom"] = None
        self.runtimeDependencies["libs/dav1d"] = None
        if CraftCore.compiler.isGCCLike():
            if not CraftCore.compiler.isAndroid:
                self.runtimeDependencies["libs/libvpx"] = None
                self.runtimeDependencies["libs/zimg"] = None
                self.runtimeDependencies["libs/x264"] = None
                if not (CraftCore.compiler.isMacOS and CraftCompiler.Architecture.x86_64):
                    self.runtimeDependencies["libs/libass"] = None
        if not CraftCore.compiler.isMacOS:
            self.buildDependencies["libs/amf"] = None
            self.buildDependencies["libs/nvidia-codecs"] = None
            self.runtimeDependencies["libs/svtav1"] = None
        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/libva"] = None
            self.runtimeDependencies["libs/libvdpau"] = None
            self.runtimeDependencies["libs/intel-mfx"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.platform = ""
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.configure.noCacheFile = True
        self.subinfo.options.configure.autoreconf = False
        # with msvc it does not support shadowbuilds
        self.subinfo.options.useShadowBuild = not CraftCore.compiler.isMSVC()

        if CraftCore.compiler.isMacOS:
            # Workaround linker bug with clang 15, see  https://github.com/homebrew-ffmpeg/homebrew-ffmpeg/issues/140
            self.subinfo.options.configure.ldflags += " -Wl,-ld_classic"

        if not CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["--enable-libmp3lame"]
        else:
            self.subinfo.options.configure.args += ["--disable-programs"]
        if "CC" in os.environ:
            cc = os.environ["CC"]
            if CraftCore.compiler.isMacOS and not CraftCore.compiler.isNative():
                cc = f"{cc} -arch {CraftCore.compiler.architecture.name.lower()}"
            self.subinfo.options.configure.args += [f"--cc={cc}"]
        if "CXX" in os.environ:
            cxx = os.environ["CXX"]
            if CraftCore.compiler.isMacOS and not CraftCore.compiler.isNative():
                cxx = f"{cxx} -arch {CraftCore.compiler.architecture.name.lower()}"
            self.subinfo.options.configure.args += [f"--cxx={cxx}"]

        architecture = CraftCore.compiler.architecture.name.lower()
        if CraftCore.compiler.isAndroid:
            if CraftCore.compiler.architecture == CraftCompiler.Architecture.arm64:
                architecture = "aarch64"
                toolchain = "aarch64-linux-android"
                compiler = "aarch64-linux-android"
            elif CraftCore.compiler.architecture == CraftCompiler.Architecture.arm32:
                architecture = "arm"
                toolchain = "arm-linux-androideabi"
                compiler = "armv7a-linux-androideabi"
            elif CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_32:
                architecture = "x86"
                toolchain = "i686-linux-android"
                compiler = "i686-linux-android"
                self.subinfo.options.configure.args += ["--disable-asm", "--enable-pic"]
            else:
                architecture = CraftCore.compiler.androidArchitecture
                toolchain = f"{CraftCore.compiler.androidArchitecture}-linux-android"
                compiler = f"{CraftCore.compiler.androidArchitecture}-linux-android"
            toolchain_path = os.path.join(os.environ["ANDROID_NDK"], "toolchains/llvm/prebuilt", os.environ.get("ANDROID_NDK_HOST", "linux-x86_64"), "bin")

            self.subinfo.options.configure.args += ["--cc=" + f"{toolchain_path}/{compiler}{CraftCore.compiler.androidApiLevel()}-clang"]
            self.subinfo.options.configure.args += ["--cxx=" + f"{toolchain_path}/{compiler}{CraftCore.compiler.androidApiLevel()}-clang++"]
            self.subinfo.options.configure.args += ["--enable-cross-compile", "--target-os=android", "--cross-prefix=llvm-"]
            # needed with NDK r25, otherwise build fails due to not finding vulkan_beta.h
            self.subinfo.options.configure.args += ["--extra-cflags=-DVK_ENABLE_BETA_EXTENSIONS=0"]

        if self.buildTarget < CraftVersion("5.0"):
            self.subinfo.options.configure.args += ["--enable-avresample"]

        if CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += ["--enable-dxva2"]
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.cflags += "-FS"
            self.subinfo.options.configure.cxxflags += "-FS"
            self.subinfo.options.configure.args += ["--toolchain=msvc"]
        elif not CraftCore.compiler.isAndroid:
            # vorbis.pc & ogg.pc currently not generated by patch to use CMake
            self.subinfo.options.configure.args += [
                "--enable-libopus",
                "--enable-libvorbis",
                "--enable-libvpx",
                "--enable-libaom",
                "--enable-libdav1d",
                "--enable-libzimg",
            ]
            if not (CraftCore.compiler.isMacOS and CraftCompiler.Architecture.x86_64):
                self.subinfo.options.configure.args += ["--enable-libass"]

        self.subinfo.options.configure.args += [
            f"--arch={architecture}",
            "--enable-shared",
            "--disable-debug",
            "--disable-doc",
            "--enable-gpl",
            "--enable-version3",
            "--enable-nonfree",
            "--enable-openssl",
        ]

        # This disables H.264/H.265 **encoding** and not decoding (that is handled by avcodec)
        # No one is encoding videos on Android (yet?) and ffmpeg doesn't pick these up properly on Android yet anyway.
        if not CraftCore.compiler.isAndroid:
            if self.subinfo.options.isActive("libs/x264"):
                self.subinfo.options.configure.args += ["--enable-libx264"]

            if self.subinfo.options.isActive("libs/x265"):
                self.subinfo.options.configure.args += ["--enable-libx265"]

        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["--enable-rpath", "--install-name-dir=@rpath"]
        elif not CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["--enable-ffnvcodec", "--enable-nvdec", "--enable-nvenc", "--enable-cuvid", "--enable-amf", "--enable-libsvtav1"]
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += ["--enable-vaapi", "--enable-vdpau"]
            if CraftCore.compiler.architecture & CraftCore.compiler.Architecture.x86:
                self.subinfo.options.configure.args += ["--enable-libmfx"]

    def configure(self):
        with utils.ScopedEnv(self._ffmpegEnv()):
            return super().configure()

    def make(self, dummyBuildType=None):
        with utils.ScopedEnv(self._ffmpegEnv()):
            return super().make()

    def install(self):
        if not super().install():
            return False

        if CraftCore.compiler.isWindows:
            files = ["avcodec", "avdevice", "avfilter", "avformat", "avresample", "avutil", "postproc", "swresample", "swscale"]
            if self.buildTarget < CraftVersion("5.0"):
                files += ["avresample"]
            for file in files:
                file += ".lib"
                src = self.installDir() / "bin" / file
                if os.path.isfile(src):
                    os.rename(src, self.installDir() / "lib" / file)

        return True

    def _ffmpegEnv(self):
        if not CraftCore.compiler.isMSVC():
            return {}
        return {
            "LIB": f"{os.environ['LIB']};{CraftStandardDirs.craftRoot() / 'lib'}",
            "INCLUDE": f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot()/ 'include'}",
        }
