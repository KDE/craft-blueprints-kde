import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.description = "Tom's LADSPA Plugins"
        self.webpage = 'http://tap-plugins.sourceforge.net'
        for ver in ['1.0.1']:
            self.targets[ver] = f'https://github.com/tomszilagyi/tap-plugins/archive/v{ver}.tar.gz'
            self.targetInstSrc[ver] = f'tap-plugins-{ver}'
            self.patchToApply[ver] = ('tap-mingw.patch', 0)
        self.targetDigests['1.0.1'] = (['89c932bea903589db2717ca4d87013fea404b4123fc71acba5bc7cba18d3ecbb'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.0.1'

    def setDependencies( self ):
        self.buildDependencies['libs/ladspa-sdk'] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.useShadowBuild = False
        inst = OsUtils.toMSysPath(self.installDir())
        self.subinfo.options.install.args += [f'INSTALL_PLUGINS_DIR={inst}/lib/ladspa/',
                                              f'INSTALL_LRDF_DIR={inst}/share/ladspa/rdf/']

    def configure(self):
        return True
