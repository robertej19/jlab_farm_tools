from setuptools import setup
from Cython.Build import cythonize

setup(
	ext_modules = cythonize(extenstions,
		language_level="3")
)
