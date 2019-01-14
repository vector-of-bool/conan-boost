from conans import ConanFile
from conans import tools
from conans.client.build.cppstd_flags import cppstd_flag
from conans.model.version import Version
from conans.errors import ConanException

import glob
import os
import sys
import shutil
import json

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

# From from *1 (see below, b2 --show-libraries), also ordered following linkage order
# see https://github.com/Kitware/CMake/blob/master/Modules/FindBoost.cmake to know the order


lib_list = ['math', 'wave', 'container', 'contract', 'exception', 'graph', 'iostreams', 'locale', 'log',
            'program_options', 'random', 'regex', 'mpi', 'serialization',
            'coroutine', 'fiber', 'context', 'timer', 'thread', 'chrono', 'date_time',
            'atomic', 'filesystem', 'system', 'graph_parallel', 'python',
            'stacktrace', 'test', 'type_erasure']


BOOST_LM_PACKAGE_NAME = 'Boost'
BOOST_LM_NAMESPACE = 'Boost'
BOOST_LMP_FILENAME = 'boost.lmp'


def boost_lm_name(name):
    return '{}/{}'.format(BOOST_LM_NAMESPACE, name)


def boost_lm_filename(name):
    return 'boost-{}.lml'.format(name)


boost_interdep = {
    'accumulators': {
        'uses': [],
    },
    'algorithm': {
        'uses': [],
    },
    'align': {
        'uses': [],
    },
    'any': {
        'uses': [],
    },
    'array': {
        'uses': [],
    },
    'asio': {
        'uses': [
            'coroutine',
            'system',
        ],
        'special-uses': ['Sockets'],
    },
    'assert': {
        'uses': [],
    },
    'assign': {
        'uses': [],
    },
    'atomic': {
        'uses': [],
    },
    'beast': {
        'uses': [],
    },
    'bimap': {
        'uses': [],
    },
    'bind': {
        'uses': [],
    },
    'callable_traits': {
        'uses': [],
    },
    'chrono': {
        'uses': [],
    },
    'circular_buffer': {
        'uses': [],
    },
    'compatibility': {
        'uses': [],
    },
    'compute': {
        'uses': [],
    },
    'concept_check': {
        'uses': [],
    },
    'config': {
        'uses': [],
    },
    'container': {
        'uses': [],
    },
    'container_hash': {
        'uses': [],
    },
    'context': {
        'uses': [],
    },
    'contract': {
        'uses': [],
    },
    'conversion': {
        'uses': [],
    },
    'convert': {
        'uses': [],
    },
    'core': {
        'uses': [],
    },
    'coroutine': {
        'uses': [],
    },
    'coroutine2': {
        'uses': [],
    },
    'crc': {
        'uses': [],
    },
    'date_time': {
        'uses': [],
    },
    'detail': {
        'uses': [],
    },
    'disjoin_sets': {
        'uses': [],
    },
    'dll': {
        'uses': [],
    },
    'dynamic_bitset': {
        'uses': [],
    },
    'endian': {
        'uses': [],
    },
    'exception': {
        'uses': [],
    },
    'fiber': {
        'uses': [],
    },
    'filesystem': {
        'uses': [],
    },
    'flyweight': {
        'uses': [],
    },
    'foreach': {
        'uses': [],
    },
    'format': {
        'uses': [],
    },
    'function': {
        'uses': [],
    },
    'function_types': {
        'uses': [],
    },
    'functional': {
        'uses': [],
    },'fusion': {
        'uses': [],
    },
    'geometry': {
        'uses': [],
    },
    'gil': {
        'uses': [],
    }, 'graph': {
        'uses': [],
    },
    'graph_parallel': {
        'uses': [],
    },
    'hana': {
        'uses': [],
    },
    'heap': {
        'uses': [],
    },
    'hof': {
        'uses': [],
    },
    'icl': {
        'uses': [],
    },
    'integer': {
        'uses': [],
    },
    'interprocess': {
        'uses': [],
    },
    'intrusive': {
        'uses': [],
    },
    'io': {
        'uses': [],
    },
    'iostreams': {
        'uses': [],
    },
    'iterator': {
        'uses': [],
    },
    'lambda': {
        'uses': [],
    },
    'lexical_cast': {
        'uses': [],
    },
    'local_function': {
        'uses': [],
    },
    'locale': {
        'uses': [],
    },
    'lockfree': {
        'uses': [],
    },
    'log': {
        'uses': [],
    },
    'logic': {
        'uses': [],
    },
    'math': {
        'uses': [],
    },
    'metaparse': {
        'uses': [],
    },
    'move': {
        'uses': [],
    },
    'mp11': {
        'uses': [],
    },
    'mpi': {
        'uses': [],
    },
    'mpl': {
        'uses': [],
    },
    'msm': {
        'uses': [],
    },
    'multi_array': {
        'uses': [],
    },
    'multi_index': {
        'uses': [],
    },
    'multiprecision': {
        'uses': [],
    },
    'numeric_conversion': {
        'uses': [],
    },
    'numeric_interval': {
        'uses': [],
    },
    'numeric_odeint': {
        'uses': [],
    },
    'numeric_ublas': {
        'uses': [],
    },
    'optional': {
        'uses': [],
    },
    'parameter': {
        'uses': [],
    },
    'parameter_python': {
        'uses': [],
    },
    'phoenix': {
        'uses': [],
    },
    'poly_collection': {
        'uses': [],
    },
    'polygon': {
        'uses': [],
    },
    'pool': {
        'uses': [],
    },
    'predef': {
        'uses': [],
    },
    'preprocessor': {
        'uses': [],
    },
    'process': {
        'uses': [],
    },
    'program_options': {
        'uses': [],
    },
    'property_map': {
        'uses': [],
    },
    'property_tree': {
        'uses': [],
    },
    'proto': {
        'uses': [],
    },
    'ptr_container': {
        'uses': [],
    },
    'python': {
        'uses': [],
    },
    'qvm': {
        'uses': [],
    },
    'random': {
        'uses': [],
    },
    'range': {
        'uses': [],
    },
    'ratio': {
        'uses': [],
    },
    'rational': {
        'uses': [],
    },
    'regex': {
        'uses': [],
    },
    'safe_numerics': {
        'uses': [],
    },
    'scope_exit': {
        'uses': [],
    },
    'serialization': {
        'uses': [],
    },
    'signals2': {
        'uses': [],
    },
    'smart_ptr': {
        'uses': [],
    },
    'sort': {
        'uses': [],
    },
    'spirit': {
        'uses': [],
    },
    'stacktrace': {
        'uses': [],
    },
    'static_assert': {
        'uses': [],
    },
    'system': {
        'uses': [],
    },
    'test': {
        'uses': [],
    },
    'thread': {
        'uses': [],
    },
    'throw_exception': {
        'uses': [],
    },
    'timer': {
        'uses': [],
    },
    'tokenizer': {
        'uses': [],
    },
    'tti': {
        'uses': [],
    },
    'tuple': {
        'uses': [],
    },
    'type_erasure': {
        'uses': [],
    },
    'type_index': {
        'uses': [],
    },
    'type_traits': {
        'uses': [],
    },
    'typeof': {
        'uses': [],
    },
    'units': {
        'uses': [],
    },
    'unordered': {
        'uses': [],
    },
    'utility': {
        'uses': [],
    },
    'uuid': {
        'uses': [],
    },
    'variant': {
        'uses': [],
    },
    'vmd': {
        'uses': [],
    },
    'wave': {
        'uses': [],
    },
    'winapi': {
        'uses': [],
    },
    'xpressive': {
        'uses': [],
    },
    'yap': {
        'uses': [],
    },
}


class BoostConan(ConanFile):
    name = "boost"
    version = "1.69.0"
    settings = "os", "arch", "compiler", "build_type", "cppstd"
    folder_name = "boost_%s" % version.replace(".", "_")
    description = "Boost provides free peer-reviewed portable C++ source libraries"
    # The current python option requires the package to be built locally, to find default Python
    # implementation
    options = {
        "shared": [True, False],
        "header_only": [True, False],
        "fPIC": [True, False],
        "skip_lib_rename": [True, False],
        "magic_autolink": [True, False],  # enables BOOST_ALL_NO_LIB
        "python_executable": "ANY",  # system default python installation is used, if None
        "python_version": "ANY"  # major.minor; computed automatically, if None
    }
    options.update({"without_%s" % libname: [True, False] for libname in lib_list})

    default_options = ["shared=False",
                       "header_only=False",
                       "fPIC=True",
                       "skip_lib_rename=False",
                       "magic_autolink=False",
                       "python_executable=None",
                       "python_version=None"]

    default_options.extend(["without_%s=False" % libname for libname in lib_list if libname != "python"])
    default_options.append("without_python=True")
    default_options.append("bzip2:shared=False")
    default_options.append("zlib:shared=False")
    default_options = tuple(default_options)

    url = "https://github.com/lasote/conan-boost"
    license = "Boost Software License - Version 1.0. http://www.boost.org/LICENSE_1_0.txt"
    short_paths = True
    no_copy_source = True

    exports = ['patches/*']

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    @property
    def zip_bzip2_requires_needed(self):
        return not self.options.without_iostreams and not self.options.header_only

    def configure(self):
        if self.zip_bzip2_requires_needed:
            self.requires("bzip2/1.0.6@conan/stable")
            self.requires("zlib/1.2.11@conan/stable")

    def package_id(self):
        if self.options.header_only:
            self.info.header_only()
        else:
            del self.info.options.python_executable  # PATH to the interpreter is not important, only version matters
            if self.options.without_python:
                del self.info.options.python_version
            else:
                self.info.options.python_version = self._python_version

    def source(self):
        if tools.os_info.is_windows:
            sha256 = "d074bcbcc0501c4917b965fc890e303ee70d8b01ff5712bae4a6c54f2b6b4e52"
            extension = ".zip"
        else:
            sha256 = "9a2c2819310839ea373f42d69e733c339b4e9a19deab6bfec448281554aa4dbb"
            extension = ".tar.gz"

        zip_name = "%s%s" % (self.folder_name, extension)
        url = "https://dl.bintray.com/boostorg/release/%s/source/%s" % (self.version, zip_name)
        tools.get(url, sha256=sha256)

        tools.patch(base_path=os.path.join(self.source_folder, self.folder_name),
                    patch_file='patches/python_base_prefix.patch', strip=1)

    ##################### BUILDING METHODS ###########################

    @property
    def _python_executable(self):
        """
        obtain full path to the python interpreter executable
        :return: path to the python interpreter executable, either set by option, or system default
        """
        exe = self.options.python_executable if self.options.python_executable else sys.executable
        return str(exe).replace('\\', '/')

    def _run_python_script(self, script):
        """
        execute python one-liner script and return its output
        :param script: string containing python script to be executed
        :return: output of the python script execution, or None, if script has failed
        """
        output = StringIO()
        command = '"%s" -c "%s"' % (self._python_executable, script)
        self.output.info('running %s' % command)
        try:
            self.run(command=command, output=output)
        except ConanException:
            self.output.info("(failed)")
            return None
        output = output.getvalue().strip()
        self.output.info(output)
        return output if output != "None" else None

    def _get_python_path(self, name):
        """
        obtain path entry for the python installation
        :param name: name of the python config entry for path to be queried (such as "include", "platinclude", etc.)
        :return: path entry from the sysconfig
        """
        # https://docs.python.org/3/library/sysconfig.html
        # https://docs.python.org/2.7/library/sysconfig.html
        return self._run_python_script("from __future__ import print_function; "
                                       "import sysconfig; "
                                       "print(sysconfig.get_path('%s'))" % name)

    def _get_python_sc_var(self, name):
        """
        obtain value of python sysconfig variable
        :param name: name of variable to be queried (such as LIBRARY or LDLIBRARY)
        :return: value of python sysconfig variable
        """
        return self._run_python_script("from __future__ import print_function; "
                                       "import sysconfig; "
                                       "print(sysconfig.get_config_var('%s'))" % name)

    def _get_python_du_var(self, name):
        """
        obtain value of python distutils sysconfig variable
        (sometimes sysconfig returns empty values, while python.sysconfig provides correct values)
        :param name: name of variable to be queried (such as LIBRARY or LDLIBRARY)
        :return: value of python sysconfig variable
        """
        return self._run_python_script("from __future__ import print_function; "
                                       "import distutils.sysconfig as du_sysconfig; "
                                       "print(du_sysconfig.get_config_var('%s'))" % name)

    def _get_python_var(self, name):
        """
        obtain value of python variable, either by sysconfig, or by distutils.sysconfig
        :param name: name of variable to be queried (such as LIBRARY or LDLIBRARY)
        :return: value of python sysconfig variable
        """
        return self._get_python_sc_var(name) or self._get_python_du_var(name)

    @property
    def _python_version(self):
        """
        obtain version of python interpreter
        :return: python interpreter version, in format major.minor
        """
        version = self._run_python_script("from __future__ import print_function; "
                                          "import sys; "
                                          "print('%s.%s' % (sys.version_info[0], sys.version_info[1]))")
        if self.options.python_version and version != self.options.python_version:
            raise Exception("detected python version %s doesn't match conan option %s" % (version,
                                                                                          self.options.python_version))
        return version

    @property
    def _python_inc(self):
        """
        obtain the result of the "sysconfig.get_python_inc()" call
        :return: result of the "sysconfig.get_python_inc()" execution
        """
        return self._run_python_script("from __future__ import print_function; "
                                       "import sysconfig; "
                                       "print(sysconfig.get_python_inc())")

    @property
    def _python_abiflags(self):
        """
        obtain python ABI flags, see https://www.python.org/dev/peps/pep-3149/ for the details
        :return: the value of python ABI flags
        """
        return self._run_python_script("from __future__ import print_function; "
                                       "import sys; "
                                       "print(getattr(sys, 'abiflags', ''))")

    @property
    def _python_includes(self):
        """
        attempt to find directory containing Python.h header file
        :return: the directory with python includes
        """
        include = self._get_python_path('include')
        plat_include = self._get_python_path('platinclude')
        include_py = self._get_python_var('INCLUDEPY')
        include_dir = self._get_python_var('INCLUDEDIR')
        python_inc = self._python_inc

        candidates = [include,
                      plat_include,
                      include_py,
                      include_dir,
                      python_inc]
        for candidate in candidates:
            if candidate:
                python_h = os.path.join(candidate, 'Python.h')
                self.output.info('checking %s' % python_h)
                if os.path.isfile(python_h):
                    self.output.info('found Python.h: %s' % python_h)
                    return candidate.replace('\\', '/')
        raise Exception("couldn't locate Python.h - make sure you have installed python development files")

    @property
    def _python_libraries(self):
        """
        attempt to find python development library
        :return: the full path to the python library to be linked with
        """
        library = self._get_python_var("LIBRARY")
        ldlibrary = self._get_python_var("LDLIBRARY")
        libdir = self._get_python_var("LIBDIR")
        multiarch = self._get_python_var("MULTIARCH")
        masd = self._get_python_var("multiarchsubdir")
        with_dyld = self._get_python_var("WITH_DYLD")
        if libdir and multiarch and masd:
            if masd.startswith(os.sep):
                masd = masd[len(os.sep):]
            libdir = os.path.join(libdir, masd)

        if not libdir:
            libdest = self._get_python_var("LIBDEST")
            libdir = os.path.join(os.path.dirname(libdest), "libs")

        candidates = [ldlibrary, library]
        library_prefixes = [""] if self.settings.compiler == "Visual Studio" else ["", "lib"]
        library_suffixes = [".lib"] if self.settings.compiler == "Visual Studio" else [".so", ".dll.a", ".a"]
        if with_dyld:
            library_suffixes.insert(0, ".dylib")

        python_version = self._python_version
        python_version_no_dot = python_version.replace(".", "")
        versions = ["", python_version, python_version_no_dot]
        abiflags = self._python_abiflags

        for prefix in library_prefixes:
            for suffix in library_suffixes:
                for version in versions:
                    candidates.append("%spython%s%s%s" % (prefix, version, abiflags, suffix))

        for candidate in candidates:
            if candidate:
                python_lib = os.path.join(libdir, candidate)
                self.output.info('checking %s' % python_lib)
                if os.path.isfile(python_lib):
                    self.output.info('found python library: %s' % python_lib)
                    return python_lib.replace('\\', '/')
        raise Exception("couldn't locate python libraries - make sure you have installed python development files")

    def build(self):
        if self.options.header_only:
            self.output.warn("Header only package, skipping build")
            return

        src = os.path.join(self.source_folder, self.folder_name)
        clean_dirs = [os.path.join(self.build_folder, "bin.v2"),
                      os.path.join(self.build_folder, "architecture"),
                      os.path.join(src, "stage"),
                      os.path.join(src, "tools", "build", "src", "engine", "bootstrap"),
                      os.path.join(src, "tools", "build", "src", "engine", "bin.ntx86"),
                      os.path.join(src, "tools", "build", "src", "engine", "bin.ntx86_64")]
        for d in clean_dirs:
            if os.path.isdir(d):
                shutil.rmtree(d)

        b2_exe = self.bootstrap()
        flags = self.get_build_flags()
        # Help locating bzip2 and zlib
        self.create_user_config_jam(self.build_folder)

        # JOIN ALL FLAGS
        b2_flags = " ".join(flags)
        full_command = "%s %s -j%s --abbreviate-paths -d2" % (b2_exe, b2_flags, tools.cpu_count())
        # -d2 is to print more debug info and avoid travis timing out without output
        sources = os.path.join(self.source_folder, self.folder_name)
        full_command += ' --debug-configuration --build-dir="%s"' % self.build_folder
        self.output.warn(full_command)

        with tools.vcvars(self.settings) if self.settings.compiler == "Visual Studio" else tools.no_op():
            with tools.chdir(sources):
                # to locate user config jam (BOOST_BUILD_PATH)
                with tools.environment_append({"BOOST_BUILD_PATH": self.build_folder}):
                    # To show the libraries *1
                    # self.run("%s --show-libraries" % b2_exe)
                    self.run(full_command)

    @property
    def _b2_os(self):
        return {"Windows": "windows",
                "WindowsStore": "windows",
                "Linux": "linux",
                "Android": "android",
                "Macos": "darwin",
                "iOS": "iphone",
                "watchOS": "iphone",
                "tvOS": "appletv",
                "FreeBSD": "freebsd",
                "SunOS": "solatis"}.get(str(self.settings.os))

    @property
    def _b2_address_model(self):
        if str(self.settings.arch) in ["x86_64", "ppc64", "ppc64le", "mips64", "armv8", "sparcv9"]:
            return "64"
        else:
            return "32"

    @property
    def _b2_binary_format(self):
        return {"Windows": "pe",
                "WindowsStore": "pe",
                "Linux": "elf",
                "Android": "elf",
                "Macos": "mach-o",
                "iOS": "mach-o",
                "watchOS": "mach-o",
                "tvOS": "mach-o",
                "FreeBSD": "elf",
                "SunOS": "elf"}.get(str(self.settings.os))

    @property
    def _b2_architecture(self):
        if str(self.settings.arch).startswith('x86'):
            return 'x86'
        elif str(self.settings.arch).startswith('ppc'):
            return 'power'
        elif str(self.settings.arch).startswith('arm'):
            return 'arm'
        elif str(self.settings.arch).startswith('sparc'):
            return 'sparc'
        elif str(self.settings.arch).startswith('mips64'):
            return 'mips64'
        elif str(self.settings.arch).startswith('mips'):
            return 'mips1'
        else:
            return None

    @property
    def _b2_abi(self):
        if str(self.settings.arch).startswith('x86'):
            return "ms" if str(self.settings.os) in ["Windows", "WindowsStore"] else "sysv"
        elif str(self.settings.arch).startswith('ppc'):
            return "sysv"
        elif str(self.settings.arch).startswith('arm'):
            return "aapcs"
        elif str(self.settings.arch).startswith('mips'):
            return "o32"
        else:
            return None

    def get_build_flags(self):

        if tools.cross_building(self.settings):
            flags = self.get_build_cross_flags()
        else:
            flags = []

        # https://www.boost.org/doc/libs/1_69_0/libs/context/doc/html/context/architectures.html
        if self._b2_os:
            flags.append("target-os=%s" % self._b2_os)
        if self._b2_architecture:
            flags.append("architecture=%s" % self._b2_architecture)
        if self._b2_address_model:
            flags.append("address-model=%s" % self._b2_address_model)
        if self._b2_binary_format:
            flags.append("binary-format=%s" % self._b2_binary_format)
        if self._b2_abi:
            flags.append("abi=%s" % self._b2_abi)

        if self.settings.compiler == "gcc":
            flags.append("--layout=system")

        if self.settings.compiler == "Visual Studio" and self.settings.compiler.runtime:
            flags.append("runtime-link=%s" % ("static" if "MT" in str(self.settings.compiler.runtime) else "shared"))

        if self.settings.os == "Windows" and self.settings.compiler == "gcc":
            flags.append("threading=multi")

        flags.append("link=%s" % ("static" if not self.options.shared else "shared"))
        if self.settings.build_type == "Debug":
            flags.append("variant=debug")
        else:
            flags.append("variant=release")

        for libname in lib_list:
            if getattr(self.options, "without_%s" % libname):
                flags.append("--without-%s" % libname)

        if self.settings.cppstd:
            toolset, _, _ = self.get_toolset_version_and_exe()
            flags.append("toolset=%s" % toolset)
            flags.append("cxxflags=%s" % cppstd_flag(
                    self.settings.get_safe("compiler"),
                    self.settings.get_safe("compiler.version"),
                    self.settings.get_safe("cppstd")
                )
            )

        # CXX FLAGS
        cxx_flags = []
        # fPIC DEFINITION
        if self.settings.os != "Windows":
            if self.options.fPIC:
                cxx_flags.append("-fPIC")

        # Standalone toolchain fails when declare the std lib
        if self.settings.os != "Android":
            try:
                if str(self.settings.compiler.libcxx) == "libstdc++":
                    flags.append("define=_GLIBCXX_USE_CXX11_ABI=0")
                elif str(self.settings.compiler.libcxx) == "libstdc++11":
                    flags.append("define=_GLIBCXX_USE_CXX11_ABI=1")
                if "clang" in str(self.settings.compiler):
                    if str(self.settings.compiler.libcxx) == "libc++":
                        cxx_flags.append("-stdlib=libc++")
                        flags.append('linkflags="-stdlib=libc++"')
                    else:
                        cxx_flags.append("-stdlib=libstdc++")
            except:
                pass

        if tools.is_apple_os(self.settings.os):
            if self.settings.get_safe("os.version"):
                cxx_flags.append(tools.apple_deployment_target_flag(self.settings.os,
                                                                    self.settings.os.version))

        if self.settings.os == "iOS":
            cxx_flags.append("-DBOOST_AC_USE_PTHREADS")
            cxx_flags.append("-DBOOST_SP_USE_PTHREADS")
            cxx_flags.append("-fvisibility=hidden")
            cxx_flags.append("-fvisibility-inlines-hidden")
            cxx_flags.append("-fembed-bitcode")

        cxx_flags = 'cxxflags="%s"' % " ".join(cxx_flags) if cxx_flags else ""
        flags.append(cxx_flags)

        return flags

    def get_build_cross_flags(self):
        arch = self.settings.get_safe('arch')
        flags = []
        self.output.info("Cross building, detecting compiler...")

        if arch.startswith('arm'):
            if 'hf' in arch:
                flags.append('-mfloat-abi=hard')
        elif arch in ["x86", "x86_64"]:
            pass
        elif arch.startswith("ppc"):
            pass
        else:
            raise Exception("I'm so sorry! I don't know the appropriate ABI for "
                            "your architecture. :'(")
        self.output.info("Cross building flags: %s" % flags)

        return flags

    @property
    def _ar(self):
        if "AR" in os.environ:
            return os.environ["AR"]
        if tools.is_apple_os(self.settings.os):
            return tools.XCRun(self.settings).ar
        return None

    @property
    def _ranlib(self):
        if "RANLIB" in os.environ:
            return os.environ["RANLIB"]
        if tools.is_apple_os(self.settings.os):
            return tools.XCRun(self.settings).ranlib
        return None

    @property
    def _cxx(self):
        if "CXX" in os.environ:
            return os.environ["CXX"]
        if tools.is_apple_os(self.settings.os):
            return tools.XCRun(self.settings).cxx
        return None

    def create_user_config_jam(self, folder):
        """To help locating the zlib and bzip2 deps"""
        self.output.warn("Patching user-config.jam")

        compiler_command = self._cxx

        contents = ""
        if self.zip_bzip2_requires_needed:
            contents = "\nusing zlib : 1.2.11 : <include>%s <search>%s <name>%s ;" % (
                self.deps_cpp_info["zlib"].include_paths[0].replace('\\', '/'),
                self.deps_cpp_info["zlib"].lib_paths[0].replace('\\', '/'),
                self.deps_cpp_info["zlib"].libs[0])

            contents += "\nusing bzip2 : 1.0.6 : <include>%s <search>%s <name>%s ;" % (
                self.deps_cpp_info["bzip2"].include_paths[0].replace('\\', '/'),
                self.deps_cpp_info["bzip2"].lib_paths[0].replace('\\', '/'),
                self.deps_cpp_info["bzip2"].libs[0])

        if not self.options.without_python:
            # https://www.boost.org/doc/libs/1_69_0/libs/python/doc/html/building/configuring_boost_build.html
            contents += "\nusing python : {version} : {executable} : {includes} :  {libraries} ;"\
                .format(version=self._python_version,
                        executable=self._python_executable,
                        includes=self._python_includes,
                        libraries=self._python_libraries)

        toolset, version, exe = self.get_toolset_version_and_exe()
        exe = compiler_command or exe  # Prioritize CXX

        # Specify here the toolset with the binary if present if don't empty parameter : :
        contents += '\nusing "%s" : "%s" : ' % (toolset, version)
        contents += ' "%s"' % exe.replace("\\", "/")

        if tools.is_apple_os(self.settings.os):
            contents += " -isysroot %s" % tools.XCRun(self.settings).sdk_path
            if self.settings.get_safe("arch"):
                contents += " -arch %s" % tools.to_apple_arch(self.settings.arch)

        contents += " : \n"
        if self._ar:
            contents += '<archiver>"%s" ' % tools.which(self._ar).replace("\\", "/")
        if self._ranlib:
            contents += '<ranlib>"%s" ' % tools.which(self._ranlib).replace("\\", "/")
        if "CXXFLAGS" in os.environ:
            contents += '<cxxflags>"%s" ' % os.environ["CXXFLAGS"]
        if "CFLAGS" in os.environ:
            contents += '<cflags>"%s" ' % os.environ["CFLAGS"]
        if "LDFLAGS" in os.environ:
            contents += '<linkflags>"%s" ' % os.environ["LDFLAGS"]
        if "ASFLAGS" in os.environ:
            contents += '<asmflags>"%s" ' % os.environ["ASFLAGS"]

        contents += " ;"

        self.output.warn(contents)
        filename = "%s/user-config.jam" % folder
        tools.save(filename,  contents)

    def get_toolset_version_and_exe(self):
        compiler_version = str(self.settings.compiler.version)
        compiler = str(self.settings.compiler)
        if self.settings.compiler == "Visual Studio":
            cversion = self.settings.compiler.version
            _msvc_version = "14.1" if Version(str(cversion)) >= "15" else "%s.0" % cversion
            return "msvc", _msvc_version, ""
        elif compiler == "gcc" and compiler_version[0] >= "5":
            # For GCC >= v5 we only need the major otherwise Boost doesn't find the compiler
            # The NOT windows check is necessary to exclude MinGW:
            if not tools.which("g++-%s" % compiler_version[0]):
                # In fedora 24, 25 the gcc is 6, but there is no g++-6 and the detection is 6.3.1
                # so b2 fails because 6 != 6.3.1. Specify the exe to avoid the smart detection
                executable = tools.which("g++")
            else:
                executable = ""
            return compiler, compiler_version[0], executable
        elif str(self.settings.compiler) in ["clang", "gcc"]:
            # For GCC < v5 and Clang we need to provide the entire version string
            return compiler, compiler_version, ""
        elif self.settings.compiler == "apple-clang":
            return "clang-darwin", compiler_version, self._cxx
        elif self.settings.compiler == "sun-cc":
            return "sunpro", compiler_version, ""
        else:
            return compiler, compiler_version, ""

    ##################### BOOSTRAP METHODS ###########################
    def _get_boostrap_toolset(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            comp_ver = self.settings.compiler.version
            return "vc%s" % ("141" if Version(str(comp_ver)) >= "15" else comp_ver)

        with_toolset = {"apple-clang": "darwin"}.get(str(self.settings.compiler),
                                                     str(self.settings.compiler))

        # fallback for the case when no unversioned gcc/clang is available
        if with_toolset in ["gcc", "clang"] and not tools.which(with_toolset):
            with_toolset = "cc"
        return with_toolset

    def bootstrap(self):
        folder = os.path.join(self.source_folder, self.folder_name, "tools", "build")
        try:
            bootstrap = "bootstrap.bat" if tools.os_info.is_windows else "./bootstrap.sh"
            with tools.vcvars(self.settings) if self.settings.compiler == "Visual Studio" else tools.no_op():
                self.output.info("Using %s %s" % (self.settings.compiler, self.settings.compiler.version))
                with tools.chdir(folder):
                    option = "" if tools.os_info.is_windows else "-with-toolset="
                    cmd = "%s %s%s" % (bootstrap, option, self._get_boostrap_toolset())
                    self.output.info(cmd)
                    self.run(cmd)
        except Exception as exc:
            self.output.warn(str(exc))
            if os.path.exists(os.path.join(folder, "bootstrap.log")):
                self.output.warn(tools.load(os.path.join(folder, "bootstrap.log")))
            raise
        return os.path.join(folder, "b2.exe") if tools.os_info.is_windows else os.path.join(folder, "b2")

    ####################################################################

    def package(self):
        # This stage/lib is in source_folder... Face palm, looks like it builds in build but then
        # copy to source with the good lib name
        out_lib_dir = os.path.join(self.folder_name, "stage", "lib")
        self.copy(pattern="*", dst="include/boost", src="%s/boost" % self.folder_name)
        if not self.options.shared:
            self.copy(pattern="*.a", dst="lib", src=out_lib_dir, keep_path=False)
        self.copy(pattern="*.so", dst="lib", src=out_lib_dir, keep_path=False, symlinks=True)
        self.copy(pattern="*.so.*", dst="lib", src=out_lib_dir, keep_path=False, symlinks=True)
        self.copy(pattern="*.dylib*", dst="lib", src=out_lib_dir, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=out_lib_dir, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=out_lib_dir, keep_path=False)

        # When first call with source do not package anything
        if not os.path.exists(os.path.join(self.package_folder, "lib")):
            return

        self.renames_to_make_cmake_find_package_happy()
        self.generate_libman_libraries()

    def renames_to_make_cmake_find_package_happy(self):
        if not self.options.skip_lib_rename:
            # CMake findPackage help
            renames = []
            for libname in os.listdir(os.path.join(self.package_folder, "lib")):
                new_name = libname
                libpath = os.path.join(self.package_folder, "lib", libname)
                if "-" in libname:
                    new_name = libname.split("-", 1)[0] + "." + libname.split(".")[-1]
                    if new_name.startswith("lib"):
                        new_name = new_name[3:]
                renames.append([libpath, os.path.join(self.package_folder, "lib", new_name)])

            for original, new in renames:
                if original != new and not os.path.exists(new):
                    self.output.info("Rename: %s => %s" % (original, new))
                    os.rename(original, new)

    def generate_libman_libraries(self):
        for libname in boost_interdep:
            self._generate_libman_lib(libname)

        # The head of the package file
        lmp_lines = [
            'Type: Package',
            'Name: {}'.format(BOOST_LM_PACKAGE_NAME),
            'Namespace: {}'.format(BOOST_LM_NAMESPACE),
            '',
        ]

        # Add lines for each generated library file
        lmp_lines += ['Library: {}'.format(boost_lm_filename(lib)) for lib in boost_interdep]

        # Write the lmp file into the package
        with open(os.path.join(self.package_folder, BOOST_LMP_FILENAME), 'w') as fd:
            fd.write('\n'.join(lmp_lines))

    def _generate_libman_lib(self, name):
        depinfo = boost_interdep[name]
        fname = boost_lm_filename(name)
        lml_dir = self.package_folder
        opath = os.path.join(lml_dir, fname)
        lines = [
            'Type: Library',
            'Name: {}'.format(name),
            'Include-Path: include/',
        ]
        # Find the linkable for the library
        linkables = glob.glob(os.path.join(self.package_folder, 'lib/*boost_{}.*'.format(name)))
        if len(linkables) > 1:
            raise RuntimeError('More than one linkable candidate for "{}"'.format(name))
        if linkables:
            relpath = os.path.relpath(linkables[0], lml_dir)
            lines.append('Path: {}'.format(relpath))

        for use in depinfo['uses']:
            assert use in boost_interdep, 'Bad package name ' + use
            lines.append('Uses: {}'.format(boost_lm_name(use)))

        for special in depinfo.get('special-uses', ()):
            lines.append('Special-Uses: {}'.format(special))

        with open(opath, 'w') as fd:
            fd.write('\n'.join(lines))

    def package_info(self):
        gen_libs = tools.collect_libs(self)

        # List of lists, so if more than one matches the lib like serialization and wserialization
        # both will be added to the list
        ordered_libs = [[] for _ in range(len(lib_list))]

        # The order is important, reorder following the lib_list order
        missing_order_info = []
        for real_lib_name in gen_libs:
            for pos, alib in enumerate(lib_list):
                if os.path.splitext(real_lib_name)[0].split("-")[0].endswith(alib):
                    ordered_libs[pos].append(real_lib_name)
                    break
            else:
                # self.output.info("Missing in order: %s" % real_lib_name)
                if "_exec_monitor" not in real_lib_name:  # https://github.com/bincrafters/community/issues/94
                    missing_order_info.append(real_lib_name)  # Assume they do not depend on other

        # Flat the list and append the missing order
        self.cpp_info.libs = [item for sublist in ordered_libs
                                      for item in sublist if sublist] + missing_order_info

        if self.options.without_test:  # remove boost_unit_test_framework
            self.cpp_info.libs = [lib for lib in self.cpp_info.libs if "unit_test" not in lib]

        self.output.info("LIBRARIES: %s" % self.cpp_info.libs)
        self.output.info("Package folder: %s" % self.package_folder)

        if not self.options.header_only and self.options.shared:
            self.cpp_info.defines.append("BOOST_ALL_DYN_LINK")
        else:
            self.cpp_info.defines.append("BOOST_USE_STATIC_LIBS")

        if not self.options.header_only:
            if not self.options.without_python:
                if not self.options.shared:
                    self.cpp_info.defines.append("BOOST_PYTHON_STATIC_LIB")

            if self.settings.compiler == "Visual Studio":
                if not self.options.magic_autolink:
                    # DISABLES AUTO LINKING! NO SMART AND MAGIC DECISIONS THANKS!
                    self.cpp_info.defines.extend(["BOOST_ALL_NO_LIB"])
                    self.output.info("Disabled magic autolinking (smart and magic decisions)")
                else:
                    self.output.info("Enabled magic autolinking (smart and magic decisions)")

                # https://github.com/conan-community/conan-boost/issues/127#issuecomment-404750974
                self.cpp_info.libs.append("bcrypt")
            elif self.settings.os == "Linux":
                # https://github.com/conan-community/conan-boost/issues/135
                self.cpp_info.libs.append("pthread")

        self.env_info.BOOST_ROOT = self.package_folder

        self.user_info.libman = json.dumps({
            'packages': [
                {
                    'name': BOOST_LM_PACKAGE_NAME,
                    'path': BOOST_LMP_FILENAME,
                },
            ],
        })
