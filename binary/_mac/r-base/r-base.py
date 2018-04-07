# -*- coding: utf-8 -*-

import info

PACKAGE_CRAN_MIRROR = 'http://ftp.gwdg.de/pub/misc/cran'
PACKAGE_PATH = '/bin/macosx/'


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"

    def setTargets(self):
        for version in ['3.3.3']:
            self.targets[version] = PACKAGE_CRAN_MIRROR + PACKAGE_PATH + 'R-' + version + '.pkg'
        self.defaultTarget = '3.3.3'  # NOTE: Last official build to work with MacOS < 10.11
        self.patchLevel['3.3.3'] = 1


from Package.BinaryPackageBase import *


# Apologies: This is a terrible HACK, but the alternatives are not any good, either.
# Buidling from source requires a) fortran b) specific versions of bzip2, and pcre. And
# c) It will result in an installation that cannot install offical R binar packages.
#
# So, instead, we hack the R installation to run from our path, which works - for the time being.
class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
        # don't use shortcut to unpack into imageDir()
        self.buildSystemType = 'custom'
        # create combined package
        self.subinfo.options.package.withCompiler = None

    def unpack(self):
        workdir = self.workDir()
        utils.cleanDirectory(workdir)
        pkgextractdir = os.path.join(workdir, 'pkgextract')
        cpioextractdir = os.path.join(workdir, 'cpioextractdir')
        for filename in self.localFileNames():  # Should be only one
            utils.system('pkgutil --expand ' + os.path.join(CraftCore.standardDirs.downloadDir(), "archives", self.package.path, filename) + " " + pkgextractdir)
            utils.cleanDirectory(cpioextractdir)
            os.chdir(cpioextractdir)
            utils.system('cat ' + pkgextractdir + '/r.pkg/Payload | gzip -dc | cpio -i')

        return True

    def install(self):
        srcdir = cpioextractdir = os.path.join(self.workDir(), 'cpioextractdir')
        dstdir = os.path.join(self.installDir() ,'lib', 'R')

        utils.cleanDirectory(dstdir)
        utils.copyDir(srcdir, dstdir)

        r_wrapper_rel = os.path.join('R.framework', 'Resources' , 'R')
        r_wrapper = os.path.join(dstdir, r_wrapper_rel)
        # make R run from relative path
        with open(r_wrapper, 'r') as file:
           content  = file.read()
        content = content.replace('/Library/Frameworks', '$(dirname $(dirname $(dirname "$0")))')
        with open(r_wrapper, 'w') as file:
           file.write(content)

        # now create a "symlink" to R's own wrapper inside PATH
        # except a symlink would not work for our dirname magic, above, so create a dummy script, instead
        # it will suffer from the same limitation of not being symlink-able, but we'll assume nobody will
        # want to do that, when it's already in PATH
        utils.cleanDirectory(os.path.join(self.installDir(), 'bin'))
        with open(os.path.join(self.installDir(), 'bin', 'R'), 'w') as file:
           file.write('#!/bin/sh\n$(dirname "$0")/' + os.path.join ('../', 'lib', 'R' , r_wrapper_rel) + ' "$@"\n')
        os.chmod(os.path.join(self.installDir(), 'bin', 'R'), 0o744)

        return True
