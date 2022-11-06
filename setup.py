from distutils.core import setup, Extension
import numpy

from Cython.Build import cythonize

package = Extension('isomap_benchmark', ['modules/objects.pyx', 'modules/benchmarks.pyx'], include_dirs=[numpy.get_include()])
setup(ext_modules=cythonize([package], language_level=3))
