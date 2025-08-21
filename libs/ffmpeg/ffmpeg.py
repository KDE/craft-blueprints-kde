import os

import info
import utils
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["6.1.1", "7.0.1", "7.1"]:
            self.targets[ver] = f"https://ffmpeg.org/releases/ffmpeg-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"ffmpeg-{ver}"
            self.patchToApply[ver] = []
        self.svnTargets["master"] = "https://git.ffmpeg.org/ffmpeg.git"

        self.targetDigests["6.1.1"] = (["5e3133939a61ef64ac9b47ffd29a5ea6e337a4023ef0ad972094b4da844e3a20"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["7.0.1"] = (["5e77e84b6434d656106fafe3bceccc77176449014f3eba24d33db3fbd0939dc9"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["7.1"] = (["fd59e6160476095082e94150ada5a6032d7dcc282fe38ce682a00c18e7820528"], CraftHash.HashAlgorithm.SHA256)

        if CraftCore.compiler.isMSVC():
            for ver in ["6.1.1", "7.0.1", "7.1"]:
                self.patchToApply[ver] = [("ffmpeg-4.4-20210413.diff", 1)]

        # https://aur.archlinux.org/cgit/aur.git/tree/040-ffmpeg-add-av_stream_get_first_dts-for-chromium.patch?h=ffmpeg-git
        # This patch is for Chromium (in QtWebEngine), it has the awful requirement for a FFmpeg with add av_stream_get_first_dts
        # This function is not upstreamed and hence requires patching, for more context see eg. https://bugs.gentoo.org/831487
        self.patchToApply["7.1"] += [("040-ffmpeg-add-av_stream_get_first_dts-for-chromium.patch", 1)]

        self.patchLevel["6.1.1"] = 2
        self.patchLevel["7.1"] = 5

        self.description = "A complete, cross-platform solution to record, convert and stream audio and video."
        self.webpage = "https://ffmpeg.org/"
        self.defaultTarget = "7.1"

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
        self.runtimeDependencies["libs/onevpl"] = None
        if CraftCore.compiler.isGCCLike():
            if not CraftCore.compiler.isAndroid:
                self.runtimeDependencies["libs/libvpx"] = None
                self.runtimeDependencies["libs/libass"] = None
                self.runtimeDependencies["libs/zimg"] = None
                self.runtimeDependencies["libs/x264"] = None
        if not CraftCore.compiler.isMacOS:
            self.buildDependencies["libs/amf"] = None
            self.buildDependencies["libs/nvidia-codecs"] = None
            self.runtimeDependencies["libs/svtav1"] = None
        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/libva"] = None
            self.runtimeDependencies["libs/libvdpau"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.platform = ""
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.configure.noCacheFile = True
        self.subinfo.options.configure.autoreconf = False
        # with msvc it does not support shadowbuilds
        self.subinfo.options.useShadowBuild = not CraftCore.compiler.isMSVC()

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
                compiler = "aarch64-linux-android"
            elif CraftCore.compiler.architecture == CraftCompiler.Architecture.arm32:
                architecture = "arm"
                compiler = "armv7a-linux-androideabi"
            elif CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_32:
                architecture = "x86"
                compiler = "i686-linux-android"
                self.subinfo.options.configure.args += ["--disable-asm", "--enable-pic"]
            else:
                architecture = CraftCore.compiler.androidArchitecture
                compiler = f"{CraftCore.compiler.androidArchitecture}-linux-android"
            toolchain_path = os.path.join(os.environ["ANDROID_NDK"], "toolchains/llvm/prebuilt", os.environ.get("ANDROID_NDK_HOST", "linux-x86_64"), "bin")

            self.subinfo.options.configure.args += ["--cc=" + f"{toolchain_path}/{compiler}{CraftCore.compiler.androidApiLevel()}-clang"]
            self.subinfo.options.configure.args += ["--cxx=" + f"{toolchain_path}/{compiler}{CraftCore.compiler.androidApiLevel()}-clang++"]
            self.subinfo.options.configure.args += ["--enable-cross-compile", "--target-os=android", "--cross-prefix=llvm-"]
            # needed with NDK r25, otherwise build fails due to not finding vulkan_beta.h
            self.subinfo.options.configure.args += ["--extra-cflags=-DVK_ENABLE_BETA_EXTENSIONS=0"]

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
                "--enable-libass",
                "--enable-libaom",
                "--enable-libdav1d",
                "--enable-libzimg",
            ]

        self.subinfo.options.configure.args += [
            f"--arch={architecture}",
            "--disable-debug",
            "--disable-doc",
            "--enable-gpl",
            "--enable-version3",
            "--enable-nonfree",
            "--enable-openssl",
            "--disable-xlib",
            f"--{CraftCore.compiler.isLinux.asEnableDisable}-libxcb",
        ]

        # This disables H.264/H.265 **encoding** and not decoding (that is handled by avcodec)
        # No one is encoding videos on Android (yet?) and ffmpeg doesn't pick these up properly on Android yet anyway.
        if not CraftCore.compiler.isAndroid:
            if self.subinfo.options.isActive("libs/x264"):
                self.subinfo.options.configure.args += ["--enable-libx264"]

            if self.subinfo.options.isActive("libs/x265"):
                self.subinfo.options.configure.args += ["--enable-libx265"]

        if CraftCore.compiler.isAndroid:
            # Work around https://github.com/android/ndk/issues/1974 in ndk26.
            # But also Vulkan video decode isn't well supported on Android anyway.
            self.subinfo.options.configure.args += ["--disable-vulkan"]

        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["--enable-rpath", "--install-name-dir=@rpath"]
        elif not CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += [
                "--enable-ffnvcodec",
                "--enable-nvdec",
                "--enable-nvenc",
                "--enable-cuvid",
                "--enable-amf",
                "--enable-libsvtav1",
            ]
            if self.subinfo.options.isActive("libs/onevpl"):
                self.subinfo.options.configure.args += ["--enable-libvpl"]

        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += ["--enable-vaapi", "--enable-vdpau"]

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
            files = ["avcodec", "avdevice", "avfilter", "avformat", "avutil", "postproc", "swresample", "swscale"]
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
            "INCLUDE": f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot() / 'include'}",
        }
