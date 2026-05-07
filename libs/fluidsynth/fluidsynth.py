import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.1.6", "2.2.3", "2.3.5", "2.5.1", "2.5.3", "2.5.4"]:
            self.targets[ver] = f"https://github.com/FluidSynth/fluidsynth/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"fluidsynth-{ver}"
        self.targetDigests["2.1.6"] = (["328fc290b5358544d8dea573f81cb1e97806bdf49e8507db067621242f3f0b8a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.2.3"] = (["b31807cb0f88e97f3096e2b378c9815a6acfdc20b0b14f97936d905b536965c4"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.3.5"] = (["f89e8e983ecfb4a5b4f5d8c2b9157ed18d15ed2e36246fa782f18abaea550e0d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.1"] = (["10b2e32ba78c72ac1384965c66df06443a4bd0ab968dcafaf8fa17086001bf03"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.3"] = (["6f247edfb4b91b927efc68c8884cec2ec345c8007afe6b59558cc52a67ef2517"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.5.4"] = (["72f5720328fe44e2e5c67813885f0a6b4b004d048bd2eeeb0c0064074ebff530"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.1.6"] = [("fluidsynth-2.1.6-20210129.diff", 1)]
        self.patchToApply["2.5.1"] = [("fluidsynth-2.5.1-20260104.diff", 1)]
        self.patchToApply["2.5.3"] = [("fluidsynth-2.5.1-20260104.diff", 1)]
        self.patchToApply["2.5.4"] = [("fluidsynth-2.5.1-20260104.diff", 1)]

        self.description = "FluidSynth is a real-time software synthesizer based on the SoundFont 2 specifications and has reached widespread distribution."
        self.webpage = "http://www.fluidsynth.org/"
        self.releaseManagerId = 10437
        self.defaultTarget = "2.5.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkgconf"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/glib"] = None
            self.runtimeDependencies["libs/libsndfile"] = None
        else:
            self.runtimeDependencies["libs/oboe"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # dbus support needs a small patch on Windows but I have no idea why you would want dbus here
        self.subinfo.options.configure.args += ["-DLIB_SUFFIX=''", "-Denable-dbus=OFF"]
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += [
                "-Dosal=cpp11",
                "-Denable-opensles=ON",
                "-Denable-oboe=ON",
                "-Denable-aufile=OFF",
                "-Denable-libsndfile=OFF",
                "-Denable-libinstpatch=OFF",
                "-Denable-alsa=OFF",
                "-Denable-pulseaudio=OFF",
                "-Denable-jack=OFF",
                "-Denable-pipewire=OFF",
                "-Denable-oss=OFF",
                "-Denable-portaudio=OFF",
                "-Denable-sdl3=OFF",
                "-Denable-ladspa=OFF",
                "-Denable-readline=OFF",
                "-Denable-network=OFF",
                "-Denable-openmp=OFF",
                "-Denable-native-dls=OFF",
            ]

    def install(self):
        if not super().install():
            return False

        if CraftCore.compiler.isAndroid:
            imageRoot = self.installDir()
            configFiles = sorted(imageRoot.glob("**/lib/cmake/fluidsynth/FluidSynthConfig.cmake"))
            if not configFiles:
                CraftCore.log.error(f"Could not find FluidSynthConfig.cmake below {imageRoot}")
                return False

            configFile = configFiles[0]
            oboeLib = CraftCore.standardDirs.craftRoot() / "lib" / f"liboboe_{CraftCore.compiler.androidAbi}.so"
            oboeIncludeDir = CraftCore.standardDirs.craftRoot() / "include"

            with open(configFile, "a", encoding="utf-8") as config:
                config.write(
                    f"""

if(ANDROID)
    if(NOT TARGET Oboe::oboe)
        add_library(Oboe::oboe SHARED IMPORTED)
        set_target_properties(Oboe::oboe PROPERTIES
            IMPORTED_LOCATION "{oboeLib}"
            INTERFACE_INCLUDE_DIRECTORIES "{oboeIncludeDir}"
        )
    endif()
    foreach(_fluidsynth_target FluidSynth::libfluidsynth FluidSynth::fluidsynth)
        if(TARGET ${{_fluidsynth_target}})
            set_property(TARGET ${{_fluidsynth_target}} APPEND PROPERTY INTERFACE_LINK_LIBRARIES Oboe::oboe)
        endif()
    endforeach()
endif()
"""
                )

        return True
