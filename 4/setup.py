from distutils.core import setup, Extension
module = Extension('myModule', ['myModule.c'])
setup(
      name='myModule',
      version='1.0',
      ext_modules=[module],
)
