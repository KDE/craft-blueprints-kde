# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Mauritius Clemens <gitlab@janitor.chat>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")
        self.options.dynamic.setDefault("buildStatic", True)

    def setTargets(self):
        self.displayName = "onnxruntime"
        self.description = " ONNX Runtime: cross-platform, high performance ML inferencing and training accelerator "
        self.webpage = "https://github.com/microsoft/onnxruntime"

        VERSION = "1.27.0"
        for ver in [VERSION]:
            self.targets[ver] = f"https://github.com/microsoft/onnxruntime/archive/refs/tags/v{ver}.zip"
            self.targetInstSrc[ver] = "onnxruntime-" + ver
            self.targetDigests[ver] = ("14146bc2a9e0597a6bbbd58be60b37d629666497408ee7de030725f79a08ba3c", CraftHash.HashAlgorithm.SHA256)
            self.targetConfigurePath[ver] = "cmake"
        self.defaultTarget = VERSION

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        # onnxruntime requires cmake >= 3.28; distro cmake can be older
        # (almalinux 9 ships 3.26). dev-utils/cmake installs an official
        # cmake.org build into the craft prefix and shims it onto PATH.
        self.buildDependencies["dev-utils/cmake"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            # Single shared onnxruntime lib with its dependencies baked in
            # (onnxruntime's own switch; buildStatic covers BUILD_SHARED_LIBS).
            "-Donnxruntime_BUILD_SHARED_LIB=ON",
            "-Donnxruntime_USE_TELEMETRY=OFF",
            f"-Donnxruntime_BUILD_UNIT_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            f"-Donnxruntime_RUN_ONNX_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            "-DBUILD_ONNX_PYTHON=OFF",
            f"-DONNX_BUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            "-DONNX_BUILD_BENCHMARKS=OFF",
            "-Donnxruntime_USE_CUDA=OFF",
            "-Donnxruntime_USE_DNNL=OFF",
            "-Donnxruntime_USE_TENSORRT=OFF",
            "-Donnxruntime_USE_MIGRAPHX=OFF",
            "-Donnxruntime_USE_AVX=OFF",
            "-Donnxruntime_USE_AVX2=OFF",
            "-Donnxruntime_USE_AVX512=OFF",
            "-DCMAKE_CXX_STANDARD=20",
            "-DCMAKE_CXX_STANDARD_REQUIRED=ON",
            "-DFETCHCONTENT_TRY_FIND_PACKAGE_MODE=NEVER",
            # Align the FetchContent deps' MSVC CRT with onnxruntime's own /MD
            # (they default to static /MT when built as static libs -> LNK4098/LNK1169).
            "-Dprotobuf_MSVC_STATIC_RUNTIME=OFF",
            "-DABSL_MSVC_STATIC_RUNTIME=OFF",
            "-DONNX_USE_MSVC_STATIC_RUNTIME=OFF",
        ]
