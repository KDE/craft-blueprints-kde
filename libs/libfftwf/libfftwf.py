# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['3.3.8'] = 'http://www.fftw.org/fftw-3.3.8.tar.gz'
        self.patchToApply['3.3.8'] = ('libfftw-win32-aligned-malloc.patch', 0)
        self.targetDigests['3.3.8'] = '59831bd4b2705381ee395e54aa6e0069b10c3626'
        self.targetInstSrc['3.3.8'] = "fftw-3.3.8"
        self.description = "a C subroutine library for computing the discrete Fourier transform (DFT)"

        self.defaultTarget = '3.3.8'

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.supportsNinja = False
        self.subinfo.options.configure.args += ' -DBUILD_TESTS=OFF'
        # -DENABLE_THREADS=ON -DENABLE_OPENMP=ON'
        self.subinfo.options.configure.args += ' -DENABLE_FLOAT=ON -DENABLE_SSE=ON'
        if CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += ' -DWITH_OUR_MALLOC=1'
