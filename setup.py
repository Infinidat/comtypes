r"""

comtypes
--------

**comtypes** is a lightweight Python COM package, based on the ctypes_
FFI library, in less than 10000 lines of code (not counting the
tests).

**comtypes** allows to define, call, and implement custom and
dispatch-based COM interfaces in pure Python.  It works on Windows,
64-bit Windows, and Windows CE.

Documentation:

    http://starship.python.net/crew/theller/comtypes/

SVN repository:

    checkout: `https://comtypes.svn.sourceforge.net/svnroot/comtypes/`_

    ViewVC: https://comtypes.svn.sourceforge.net/comtypes/

Mailing list:

    http://gmane.org/info.php?group=gmane.comp.python.comtypes.user

    https://lists.sourceforge.net/lists/listinfo/comtypes-users/

Releases can be downloaded in the sourceforge files_ section.

.. _files: http://sourceforge.net/project/showfiles.php?group_id=115265

.. _`https://comtypes.svn.sourceforge.net/svnroot/comtypes/`: https://comtypes.svn.sourceforge.net/svnroot/comtypes/#egg=comtypes-dev

.. _ctypes: http://docs.python.org/lib/module-ctypes.html
"""
import sys, os
from distutils.core import setup, Command, DistutilsOptionError

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

class test(Command):
    # Original version of this class posted
    # by Berthold Hoellmann to distutils-sig@python.org
    description = "run tests"

    user_options = [
        ('tests=', 't',
         "comma-separated list of packages that contain test modules"),
        ('use-resources=', 'u',
         "resources to use - resource names are defined by tests"),
        ('refcounts', 'r',
         "repeat tests to search for refcount leaks (requires 'sys.gettotalrefcount')"),
        ]

    boolean_options = ["refcounts"]

    def initialize_options(self):
        self.use_resources = ""
        self.refcounts = False
        self.tests = "comtypes.test"

    # initialize_options()

    def finalize_options(self):
        if self.refcounts and not hasattr(sys, "gettotalrefcount"):
            raise DistutilsOptionError("refcount option requires Python debug build")
        self.tests = self.tests.split(",")
        self.use_resources = self.use_resources.split(",")

    # finalize_options()

    def run(self):
        build = self.reinitialize_command('build')
        build.run()
        if build.build_lib is not None:
            sys.path.insert(0, build.build_lib)

        import comtypes.test
        comtypes.test.use_resources.extend(self.use_resources)

        for name in self.tests:
            package = __import__(name, globals(), locals(), ['*'])
            sys.stdout.write("Testing package %s %s\n"
                             % (name, (sys.version, sys.platform, os.name)))
            comtypes.test.run_tests(package,
                                    "test_*.py",
                                    self.verbose,
                                    self.refcounts)

    # run()

# class test

classifiers = [
##    'Development Status :: 3 - Alpha',
    'Development Status :: 4 - Beta',
##    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
##    'Operating System :: Microsoft :: Windows CE', # pypi doesn't have this classifier
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ]

def read_version():
    # Determine the version number by reading it from the file
    # 'comtypes\__init__.py'.  We cannot import this file (with py3,
    # at least) because it is in py2.x syntax.
    ns = {}
    for line in open("comtypes\__init__.py"):
        if line.startswith("__version__ = "):
            exec(line, ns)
            break
    return ns["__version__"]

setup(name="comtypes",
      description="Pure Python COM package",
      long_description = __doc__,
      author="Thomas Heller",
      author_email="theller@python.net",
      url="http://starship.python.net/crew/theller/comtypes",
      download_url = "http://sourceforge.net/project/showfiles.php?group_id=115265",

      license="MIT License",
      package_data = {"comtypes.test": ["TestComServer.idl",
                                        "TestComServer.tlb"]},
      classifiers=classifiers,

      scripts=["clear_comtypes_cache.py"],
      options={"bdist_wininst": {"install_script": "clear_comtypes_cache.py"}},

      cmdclass = {'test': test,
                  'build_py': build_py},

      version=read_version(),
      packages=["comtypes",
                "comtypes.client",
                "comtypes.server",
                "comtypes.tools",
                "comtypes.test"])
