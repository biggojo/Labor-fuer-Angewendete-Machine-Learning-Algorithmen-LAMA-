from distutils.core import setup, Extension

module1 = Extension('lama_blackbox', sources = ['main.c'])

setup (name = "LAMA's BlackBox",
        version = '1.0',
        description = 'LAMA Blackbox Package',
        ext_modules = [module1])
