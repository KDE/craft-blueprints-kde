# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/libgit2/libgit2.git'

        self.description = "a portable C library for accessing git repositories"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.buildDependencies['dev-util/pkg-config'] = 'default'
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies['libs/win_iconv'] = 'default'
        self.runtimeDependencies['libs/libssh2'] = 'default'
        self.runtimeDependencies['libs/openssl'] = 'default'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DUSE_ICONV=ON -DBUILD_CLAR=OFF"

# self.subinfo.options.configure.args = "-DDBUS_REPLACE_LOCAL_DIR=ON "
