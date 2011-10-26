from zorg.buildbot.builders import ClangBuilder
reload(ClangBuilder)
from zorg.buildbot.builders import ClangBuilder

from zorg.buildbot.builders import LLVMBuilder
reload(LLVMBuilder)
from zorg.buildbot.builders import LLVMBuilder

from zorg.buildbot.builders import LLVMGCCBuilder
reload(LLVMGCCBuilder)
from zorg.buildbot.builders import LLVMGCCBuilder

from zorg.buildbot.builders import DragonEggBuilder
reload(DragonEggBuilder)
from zorg.buildbot.builders import DragonEggBuilder

from zorg.buildbot.builders import NightlytestBuilder
reload(NightlytestBuilder)
from zorg.buildbot.builders import NightlytestBuilder

from zorg.buildbot.builders import ScriptedBuilder
reload(ScriptedBuilder)
from zorg.buildbot.builders import ScriptedBuilder

from zorg.buildbot.builders import PollyBuilder
reload(PollyBuilder)
from zorg.buildbot.builders import PollyBuilder

from zorg.buildbot.builders import LLDBBuilder
reload(LLDBBuilder)
from zorg.buildbot.builders import LLDBBuilder

from buildbot.steps.source import SVN
from zorg.buildbot.commands.ClangTestCommand import ClangTestCommand

# Plain LLVM builders.
def _get_llvm_builders():
    return [
#        {'name': "llvm-i686-linux",
#         'slavenames': ["dunbar1"],
#         'builddir': "llvm-i686",
#         'factory': LLVMBuilder.getLLVMBuildFactory("i686-pc-linux-gnu", jobs=2, enable_shared=True)},
        {'name': "llvm-x86_64-linux",
         'slavenames': ["gcc14"],
         'builddir': "llvm-x86_64",
         'factory': LLVMBuilder.getLLVMBuildFactory(triple="x86_64-pc-linux-gnu")},
        {'name': "llvm-arm-linux",
         'slavenames':["ranby1"],
         'builddir':"llvm-arm-linux",
         'factory': LLVMBuilder.getLLVMBuildFactory("arm-pc-linux-gnu", jobs=1, clean=True,
                                                    timeout=40)},
        {'name': "llvm-ppc-darwin",
         'slavenames':["arxan_bellini"],
         'builddir':"llvm-ppc-darwin",
         'factory': LLVMBuilder.getLLVMBuildFactory("ppc-darwin", jobs=1, clean=True,
                            config_name = 'Release',
                            env = { 'CC' : "/usr/bin/gcc-4.2",
                                    'CXX': "/usr/bin/g++-4.2" },
                            extra_configure_args=['--enable-shared'],
                            timeout=600)},
        {'name': "llvm-i686-debian",
         'slavenames': ["gcc15"],
         'builddir': "llvm-i686-debian",
         'factory': LLVMBuilder.getLLVMBuildFactory("i686-pc-linux-gnu",
                                                     env = { 'CC' : "gcc -m32",  'CXX' : "g++ -m32" })},
        {'name': "llvm-x86_64-ubuntu",
         'slavenames':["arxan_davinci"],
         'builddir':"llvm-x86_64-ubuntu",
         'factory': LLVMBuilder.getLLVMBuildFactory("x86_64-pc-linux-gnu", jobs=4)},
        ]

# Offline.
{'name': "llvm-alpha-linux",
 'slavenames':["andrew1"],
 'builddir':"llvm-alpha",
 'factory': LLVMBuilder.getLLVMBuildFactory("alpha-linux-gnu", jobs=2)}
{'name': "llvm-i386-auroraux",
 'slavenames':["evocallaghan"],
 'builddir':"llvm-i386-auroraux",
 'factory': LLVMBuilder.getLLVMBuildFactory("i386-pc-auroraux", jobs="%(jobs)s", make='gmake')},
{'name': "llvm-ppc-linux",
 'slavenames':["nick1"],
 'builddir':"llvm-ppc",
 'factory': LLVMBuilder.getLLVMBuildFactory("ppc-linux-gnu", jobs=1, clean=False, timeout=40)},

# llvm-gcc self hosting builders.
def _get_llvmgcc_builders():
    return [
#        {'name' : "llvm-gcc-i686-darwin10-selfhost",
#         'slavenames':["dunbar-darwin10"],
#         'builddir':"llvm-gcc-i686-darwin10-selfhost",
#         'factory':LLVMGCCBuilder.getLLVMGCCBuildFactory(4, triple='i686-apple-darwin10',
#                                                         gxxincludedir='/usr/include/c++/4.2.1')},
        {'name' : "llvm-gcc-i386-linux-selfhost",
         'slavenames':["gcc11"],
         'builddir':"llvm-gcc-i386-linux-selfhost",
         'factory':LLVMGCCBuilder.getLLVMGCCBuildFactory(triple='i686-pc-linux-gnu',
                                                         extra_languages="fortran",
                                                         env = { 'CC'             : "gcc -m32",
                                                                 'CXX'            : "g++ -m32",
                                                                 'LD_LIBRARY_PATH': "/home/baldrick/lib32/",
                                                                 'LIBRARY_PATH'   : "/emul/ia32-linux/usr/lib/:/home/baldrick/lib32/",
                                                                 'PATH'           : "/home/baldrick/bin32:/usr/bin:/bin"
                                                                 },
                                                         extra_configure_args=['--disable-multilib',
                                                         '--enable-targets=all',
                                                         '--with-as=/home/baldrick/bin32/as',
                                                         '--with-mpfr=/home/baldrick/cfarm-32',
                                                         '--with-gmp=/home/baldrick/cfarm-32'])},
#        {'name' : "llvm-gcc-x86_64-darwin10-selfhost",
#         'slavenames':["dunbar-darwin10"],
#         'builddir':"llvm-gcc-x86_64-darwin10-selfhost",
#         'factory':LLVMGCCBuilder.getLLVMGCCBuildFactory(4, triple='x86_64-apple-darwin10',
#                                                         gxxincludedir='/usr/include/c++/4.2.1')},

        {'name' : "llvm-x86_64-linux-checks",
         'slavenames':["gcc10"],
         'builddir':"llvm-x86_64-linux-checks",
         'factory':LLVMGCCBuilder.getLLVMGCCBuildFactory(triple='x86_64-pc-linux-gnu',
                                                         stage1_config='Release+Asserts+Checks',
                                                         stage2_config='Debug+Asserts+Checks',
                                                         extra_languages="fortran",
                                                         extra_configure_args=['--disable-multilib',
                                                         '--with-mpfr=/opt/cfarm/mpfr',
                                                         '--with-gmp=/opt/cfarm/gmp'],
                                                         timeout=120)},
        ]

clang_i386_linux_xfails = [
    'GCCAS.MultiSource/Benchmarks/tramp3d-v4/tramp3d-v4',
    'Bytecode.MultiSource/Benchmarks/tramp3d-v4/tramp3d-v4',
    'LLC.MultiSource/Applications/oggenc/oggenc',
    'LLC.MultiSource/Benchmarks/VersaBench/bmm/bmm',
    'LLC.MultiSource/Benchmarks/VersaBench/dbms/dbms',
    'LLC.MultiSource/Benchmarks/tramp3d-v4/tramp3d-v4',
    'LLC.SingleSource/Benchmarks/Misc-C++/Large/sphereflake',
    'LLC.SingleSource/Regression/C++/EH/ConditionalExpr',
    'LLC_compile.MultiSource/Applications/oggenc/oggenc',
    'LLC_compile.MultiSource/Benchmarks/VersaBench/bmm/bmm',
    'LLC_compile.MultiSource/Benchmarks/VersaBench/dbms/dbms',
    'LLC_compile.MultiSource/Benchmarks/tramp3d-v4/tramp3d-v4',
    'LLC_compile.SingleSource/Benchmarks/Misc-C++/Large/sphereflake',
    'LLC_compile.SingleSource/Regression/C++/EH/ConditionalExpr',
]

clang_x86_64_linux_xfails = [
    'LLC.SingleSource/Regression/C++/EH/ConditionalExpr',
    'LLC.SingleSource/UnitTests/Vector/SSE/sse.expandfft',
    'LLC.SingleSource/UnitTests/Vector/SSE/sse.stepfft',
    'LLC_compile.SingleSource/Regression/C++/EH/ConditionalExpr',
    'LLC_compile.SingleSource/UnitTests/Vector/SSE/sse.expandfft',
    'LLC_compile.SingleSource/UnitTests/Vector/SSE/sse.stepfft',
]

# Clang builders.
def _get_clang_builders():
    return [
#        {'name': "clang-x86_64-linux",
#         'slavenames':["gcc14"],
#         'builddir':"clang-x86_64-linux",
#         'factory': ClangBuilder.getClangBuildFactory(examples=True)},
#        {'name': "clang-i686-linux",
#         'slavenames':["dunbar1"],
#         'builddir':"clang-i686-linux",
#         'factory': ClangBuilder.getClangBuildFactory()},
        {'name': "clang-arm-linux",
         'slavenames':["nick3"],
         'builddir':"clang-arm-linux",
         'factory': ClangBuilder.getClangBuildFactory()},
#        {'name' : "clang-i686-darwin10",
#         'slavenames' :["dunbar-darwin10"],
#         'builddir' :"clang-i686-darwin10",
#         'factory': ClangBuilder.getClangBuildFactory(triple='i686-apple-darwin10',
#                                                      stage1_config='Release')},
        {'name': "clang-i686-freebsd",
         'slavenames':["freebsd1"],
         'builddir':"clang-i686-freebsd",
         'factory': ClangBuilder.getClangBuildFactory(clean=True, use_pty_in_tests=True)},
#        {'name' : "clang-i686-xp-msvc9",
#         'slavenames' :['dunbar-win32-2'],
#         'builddir' :"clang-i686-xp-msvc9",
#         'factory' : ClangBuilder.getClangMSVCBuildFactory(jobs=2)},
#        {'name' : "clang-x86_64-darwin10-selfhost",
#         'slavenames' : ["dunbar-darwin10"],
#         'builddir' : "clang-x86_64-darwin10-selfhost",
#         'factory' : ClangBuilder.getClangBuildFactory(triple='x86_64-apple-darwin10',
#                                                       useTwoStage=True,
#                                                       stage1_config='Release+Asserts',
#                                                       stage2_config='Debug+Asserts')},

        {'name' : "clang-i686-linux-fnt",
         'slavenames' : ['balint1'],
         'builddir' : "clang-i686-linux-fnt",
         'factory' : NightlytestBuilder.getFastNightlyTestBuildFactory(triple='i686-pc-linux-gnu',
                                                                       stage1_config='Release+Asserts',
                                                                       test=False,
                                                                       xfails=clang_i386_linux_xfails) },

        {'name': "clang-x86_64-debian",
         'slavenames':["gcc12"],
         'builddir':"clang-x86_64-debian",
         'factory': ClangBuilder.getClangBuildFactory()},

        {'name' : "clang-x86_64-debian-selfhost-rel",
         'slavenames' : ["gcc13"],
         'builddir' : "clang-x86_64-debian-selfhost-rel",
         'factory' : ClangBuilder.getClangBuildFactory(triple='x86_64-pc-linux-gnu',
                                                       useTwoStage=True,
                                                       stage1_config='Release+Asserts',
                                                       stage2_config='Release+Asserts')},

        {'name' : "clang-x86_64-debian-fnt",
         'slavenames' : ['gcc20'],
         'builddir' : "clang-x86_64-debian-fnt",
         'factory' : NightlytestBuilder.getFastNightlyTestBuildFactory(triple='x86_64-pc-linux-gnu',
                                                                       stage1_config='Release+Asserts',
                                                                       test=False,
                                                                       xfails=clang_x86_64_linux_xfails) },
        ]

# Offline.
{'name': "clang-i386-auroraux",
 'slavenames':["evocallaghan"],
 'builddir':"clang-i386-auroraux",
 'factory': ClangBuilder.getClangBuildFactory("i386-pc-auroraux",
                                              jobs="%(jobs)s", make='gmake')},

def _get_dragonegg_builders():
    return [
        {'name' : 'dragonegg-i386-linux',
         'slavenames' : ['gcc16'],
         'builddir' : 'dragonegg-i386-linux',
         'factory'   : ScriptedBuilder.getScriptedBuildFactory(
                       source_code  = [SVN(name='svn-llvm',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm/',
                                           defaultBranch='trunk',
                                           workdir="llvm.src"),
                                       SVN(name='svn-dragonegg',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/dragonegg/',
                                           defaultBranch='trunk',
                                           workdir="dragonegg.src"),],
                       launcher     = 'dragonegg.src/extras/buildbot_self_strap-32',
                       timeout      = 60),
         'category'  : 'dragonegg'},

        {'name' : 'dragonegg-x86_64-linux',
         'slavenames' : ['gcc17'],
         'builddir' : 'dragonegg-x86_64-linux',
         'factory'   : ScriptedBuilder.getScriptedBuildFactory(
                       source_code  = [SVN(name='svn-llvm',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm/',
                                           defaultBranch='trunk',
                                           workdir="llvm.src"),
                                       SVN(name='svn-dragonegg',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/dragonegg/',
                                           defaultBranch='trunk',
                                           workdir="dragonegg.src"),],
                       launcher     = 'dragonegg.src/extras/buildbot_self_strap',
                       timeout      = 60),
         'category'  : 'dragonegg'},

        ]

# Polly builders.
def _get_polly_builders():
    return [
        {'name': "polly-amd64-linux",
         'slavenames':["grosser1"],
         'builddir':"polly-amd64-linux",
         'factory': PollyBuilder.getPollyBuildFactory()}
       ]

# LLDB builders.
def _get_lldb_builders():
    gcc_latest_env = {
        'PATH': '/opt/cfarm/python2-latest/bin:/usr/local/bin:/usr/bin:/bin:/usr/games',
        'CC':  '/opt/cfarm/release/4.5.1/bin/gcc',
        'CXX': '/opt/cfarm/release/4.5.1/bin/g++'}

    gcc_m32_latest_env = gcc_latest_env.copy()
    gcc_m32_latest_env['CC'] += ' -m32'
    gcc_m32_latest_env['CXX'] += ' -m32'

    return [
        {'name': "lldb-x86_64-linux",
         'slavenames': ["gcc14"],
         'builddir': "lldb-x86_64",
         'factory': LLDBBuilder.getLLDBBuildFactory(triple="x86_64-pc-linux-gnu",
                                                    env=gcc_latest_env)},
        {'name': "lldb-i686-debian",
         'slavenames': ["gcc15"],
         'builddir': "lldb-i686-debian",
         'factory': LLDBBuilder.getLLDBBuildFactory(triple="i686-pc-linux-gnu",
                                                    env=gcc_m32_latest_env)}
       ]

def _get_experimental_builders():
    return [

#        {'name' : "clang-i386-darwin10-selfhost-rel",
#         'slavenames' : ["dunbar-darwin10"],
#         'builddir' : "clang-i386-darwin10-selfhost-rel",
#         'factory' : ClangBuilder.getClangBuildFactory(triple='i386-apple-darwin10',
#                                                       useTwoStage=True,
#                                                       stage1_config='Release+Asserts',
#                                                       stage2_config='Release+Asserts'),
#         'category' : 'clang.exp' },
#        {'name' : "clang-x86_64-darwin10-selfhost-rel",
#         'slavenames' : ["dunbar-darwin10"],
#         'builddir' : "clang-x86_64-darwin10-selfhost-rel",
#         'factory' : ClangBuilder.getClangBuildFactory(triple='x86_64-apple-darwin10',
#                                                       useTwoStage=True,
#                                                       stage1_config='Release+Asserts',
#                                                       stage2_config='Release+Asserts'),
#         'category' : 'clang.exp' },

        {'name': "clang-native-arm-cortex-a9",
         'slavenames':["kistanova6"],
         'builddir':"clang-native-arm-cortex-a9",
         'factory' : ClangBuilder.getClangBuildFactory(
                     extra_configure_args=['--build=armv7l-unknown-linux-gnueabi',
                                           '--host=armv7l-unknown-linux-gnueabi',
                                           '--target=armv7l-unknown-linux-gnueabi',
                                           '--with-cpu=cortex-a9',
                                           '--with-fpu=neon', '--with-abi=aapcs',
                                           '--with-float=hard',
                                           '--enable-targets=arm,cbe',
                                           '--enable-optimized']),
         'category' : 'clang'},

        {'name': "clang-X86_64-freebsd",
         'slavenames':["kistanova7"],
         'builddir':"clang-X86_64-freebsd",
         'factory': NightlytestBuilder.getFastNightlyTestBuildFactory(triple='x86_64-unknown-freebsd8.2',
                                                                       stage1_config='Release+Asserts',
                                                                       test=True),
         'category' : 'clang'},

        {'name': "clang-native-mingw32-win7",
         'slavenames':["kistanova8"],
         'builddir':"clang-native-mingw32-win7",
         'factory' : ClangBuilder.getClangBuildFactory(triple='i686-pc-mingw32',
                                                       useTwoStage=True, test=True,
                                                       stage1_config='Release+Asserts',
                                                       stage2_config='Release+Asserts'),
         'category' : 'clang'},

        # Clang cross builders.
        {'name': "clang-x86_64-darwin10-self-mingw32",
         'slavenames':["kistanova1"],
         'builddir':"clang-x86_64-darwin10-self-mingw32",
         'factory' : ClangBuilder.getClangBuildFactory(outOfDir=True, jobs=4, test=False,
                                                       extra_configure_args=['--build=x86_64-apple-darwin10',
                                                                             '--host=i686-pc-mingw32',
                                                                             '--target=i686-pc-mingw32']),
         'category' : 'clang'},

        {'name' : "clang-x86_64-darwin10-cross-mingw32",
         'slavenames' :["kistanova1"],
         'builddir' :"clang-x86_64-darwin10-cross-mingw32",
         'factory' : ClangBuilder.getClangBuildFactory(outOfDir=True, jobs=4,  use_pty_in_tests=True,
                                                       run_cxx_tests=True,
                                                       extra_configure_args=['--build=x86_64-apple-darwin10',
                                                                             '--host=x86_64-apple-darwin10',
                                                                             '--target=i686-pc-mingw32']),
         'category' : 'clang'},

        # Llvm-gcc cross builders.
        {'name'      : "build-self-4-mingw32",
         'slavenames': [ "kistanova1" ],
         'builddir'  : "build-self-4-mingw32",
         'factory'   : ScriptedBuilder.getScriptedBuildFactory(
                       source_code  = [SVN(name='svn-llvm',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm/',
                                           defaultBranch='trunk',
                                           workdir="llvm.src"),
                                       SVN(name='svn-llvm-gcc',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm-gcc-4.2/',
                                           defaultBranch='trunk',
                                           workdir="llvm-gcc.src"),],
                       launcher     = 'llvm-gcc.src/extras/buildbot-launcher',
                       build_script = 'llvm-gcc.src/extras/build-self-4-mingw32',
                       extra_args   = [],
                       build_steps  = [{'name'          : 'clean',
                                        'description'   : 'clean',
                                        'haltOnFailure' : True },
                                       {'name'          : 'copy_cross_tools',
                                        'description'   : 'copy cross-tools',
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvm_1',
                                        'description'   : 'configure llvm (stage1)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvm_1',
                                        'description'   : 'compile llvm (stage1)',
                                        'extra_args'    : ['-j8'],  # Extra step-specific properties
                                        'haltOnFailure' : True },
                                       {'name'          : 'test_llvm_1',
                                        'type'          : ClangTestCommand,
                                        'description'   : 'test llvm (stage1)',
                                        'haltOnFailure' : False },
                                       {'name'          : 'configure_llvmgcc_1',
                                        'description'   : 'configure llvm-gcc (stage1)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvmgcc_1',
                                        'description'   : 'compile llvm-gcc (stage1)',
                                        'extra_args'    : ['-j8'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvmgcc_1',
                                        'description'   : 'install llvm-gcc (stage1)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvm_2',
                                        'description'   : 'configure llvm (stage2)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvm_2',
                                        'description'   : 'compile llvm (stage2)',
                                        'extra_args'    : ['-j8'],  # Extra step-specific properties
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvmgcc_2',
                                        'description'   : 'configure llvm-gcc (stage2)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvmgcc_2',
                                        'description'   : 'compile llvm-gcc (stage2)',
                                        'extra_args'    : ['-j8'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvmgcc_2',
                                        'description'   : 'install llvm-gcc (stage2)',
                                        'haltOnFailure' : True },]),
          'category'  : 'llvm-gcc' },

        {'name'      : "llvm-gcc-x86_64-darwin10-cross-i686-linux",
         'slavenames': [ "kistanova1" ],
         'builddir'  : "llvm-gcc-x86_64-darwin10-cross-i686-linux",
         'factory'   : ScriptedBuilder.getScriptedBuildFactory(
                       source_code  = [SVN(name='svn-llvm',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm/',
                                           defaultBranch='trunk',
                                           workdir="llvm.src"),
                                       SVN(name='svn-llvm-gcc',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm-gcc-4.2/',
                                           defaultBranch='trunk',
                                           workdir="llvm-gcc.src"),],
                       launcher     = 'llvm-gcc.src/extras/buildbot-launcher',
                       build_script = 'llvm-gcc.src/extras/build-x-4-linux',
                       extra_args   = [],
                       build_steps  = [{'name'          : 'clean',
                                        'description'   : 'clean',
                                        'haltOnFailure' : True },
                                       {'name'          : 'copy_cross_tools',
                                        'description'   : 'copy cross-tools',
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvm',
                                        'description'   : 'configure llvm',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvm',
                                        'description'   : 'make llvm',
                                        'extra_args'    : ['-j8'],  # Extra step-specific properties
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvmgcc',
                                        'description'   : 'configure llvm-gcc',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvmgcc',
                                        'description'   : 'make llvm-gcc',
                                        'extra_args'    : ['-j8'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvmgcc',
                                        'description'   : 'install llvm-gcc',
                                        'haltOnFailure' : True },]),
         'category'  : 'llvm-gcc' },

        {'name'      : "llvm-gcc-build-x86_64-darwin10-x-mingw32-x-armeabi",
         'slavenames': [ "kistanova1" ],
         'builddir'  : "llvm-gcc-build-x86_64-darwin10-x-mingw32-x-armeabi",
         'factory'   : ScriptedBuilder.getScriptedBuildFactory(
                       source_code  = [SVN(name='svn-llvm',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm/',
                                           defaultBranch='trunk',
                                           workdir="llvm.src"),
                                       SVN(name='svn-llvm-gcc',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm-gcc-4.2/',
                                           defaultBranch='trunk',
                                           workdir="llvm-gcc.src"),],
                       launcher     = 'llvm-gcc.src/extras/buildbot-launcher',
                       build_script = 'llvm-gcc.src/extras/build-darwin-x-mingw32-x-armeabi',
                       extra_args   = [],
                       build_steps  = [{'name'          : 'clean',
                                        'description'   : 'clean',
                                        'haltOnFailure' : True },
                                       {'name'          : 'copy_cross_tools',
                                        'description'   : 'copy cross_tools',
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvm_1',
                                        'description'   : 'configure llvm (stage 1)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvm_1',
                                        'description'   : 'make llvm (stage 1)',
                                        'extra_args'    : ['-j8'],  # Extra step-specific properties
                                        'haltOnFailure' : True },
                                       {'name'          : 'test_llvm_1',
                                        'description'   : 'test llvm (stage 1)',
                                        'haltOnFailure' : False },
                                       {'name'          : 'configure_llvmgcc_1',
                                        'description'   : 'configure llvm-gcc (stage 1)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvmgcc_1',
                                        'description'   : 'make llvm-gcc (stage 1)', # Note: one thread only here
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvmgcc_1',
                                        'description'   : 'install llvm-gcc (stage 1)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvm_2',
                                        'description'   : 'configure llvm (stage 2)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvm_2',
                                        'description'   : 'make llvm (stage 2)',
                                        'extra_args'    : ['-j8'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvmgcc_2',
                                        'description'   : 'configure llvm-gcc (stage 2)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvmgcc_2',
                                        'description'   : 'make llvm-gcc (stage 2)',
                                        'extra_args'    : ['-j8'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvmgcc_2',
                                        'description'   : 'install llvm-gcc (stage 2)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvm_3',
                                        'description'   : 'configure llvm (stage 3)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvm_3',
                                        'description'   : 'make llvm (stage 3)',
                                        'extra_args'    : ['-j8'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvmgcc_3',
                                        'description'   : 'configure llvm-gcc (stage 3)',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvmgcc_3',
                                        'description'   : 'make llvm-gcc (stage 3)',
                                        'extra_args'    : ['-j8'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvmgcc_3',
                                        'description'   : 'install llvm-gcc (stage 3)',
                                        'haltOnFailure' : True },]),

         'category'  : 'llvm-gcc' },

        {'name'      : "llvm-gcc-native-mingw32",
         'slavenames': [ "kistanova2" ],
         'builddir'  : "llvm-gcc-native-mingw32",
         'factory'   : ScriptedBuilder.getScriptedBuildFactory(
                       source_code  = [SVN(name='svn-llvm',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm/',
                                           defaultBranch='trunk',
                                           workdir="llvm.src"),
                                       SVN(name='svn-llvm-gcc',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm-gcc-4.2/',
                                           defaultBranch='trunk',
                                           workdir="llvm-gcc.src"),],
                       launcher     = 'llvm-gcc.src/extras/buildbot-launcher',
                       build_script = 'llvm-gcc.src/extras/build-native-mingw32',
                       extra_args   = [],
                       build_steps  = [{'name'          : 'clean',
                                        'description'   : 'clean',
                                        'haltOnFailure' : True },
                                       {'name'          : 'copy_tools',
                                        'description'   : 'copy tools',
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvm',
                                        'description'   : 'configure llvm',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvm',
                                        'description'   : 'make llvm',
                                        'haltOnFailure' : True },
                                       {'name'          : 'test_llvm',
                                        'type'          : ClangTestCommand,
                                        'description'   : 'test llvm',
                                        'haltOnFailure' : False },
                                       {'name'          : 'configure_llvmgcc',
                                        'description'   : 'configure llvm-gcc',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvmgcc',
                                        'description'   : 'make llvm-gcc',
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvmgcc',
                                        'description'   : 'install llvm-gcc',
                                        'haltOnFailure' : True },]),
         'category'  : 'llvm-gcc' },

        {'name'      : "llvm-gcc-native-mingw32-win7",
         'slavenames': [ "kistanova3" ],
         'builddir'  : "llvm-gcc-native-mingw32-win7",
         'factory'   : ScriptedBuilder.getScriptedBuildFactory(
                       source_code  = [SVN(name='svn-llvm',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm/',
                                           defaultBranch='trunk',
                                           workdir="llvm.src"),
                                       SVN(name='svn-llvm-gcc',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm-gcc-4.2/',
                                           defaultBranch='trunk',
                                           workdir="llvm-gcc.src"),],
                       launcher     = 'llvm-gcc.src/extras/buildbot-launcher',
                       build_script = 'llvm-gcc.src/extras/build-native-mingw32',
                       extra_args   = [],
                       build_steps  = [{'name'          : 'clean',
                                        'description'   : 'clean',
                                        'haltOnFailure' : True },
                                       {'name'          : 'copy_tools',
                                        'description'   : 'copy tools',
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvm',
                                        'description'   : 'configure llvm',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvm',
                                        'description'   : 'make llvm',
                                        'haltOnFailure' : True },
                                       {'name'          : 'test_llvm',
                                        'type'          : ClangTestCommand,
                                        'description'   : 'test llvm',
                                        'haltOnFailure' : False },
                                       {'name'          : 'configure_llvmgcc',
                                        'description'   : 'configure llvm-gcc',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvmgcc',
                                        'description'   : 'make llvm-gcc',
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvmgcc',
                                        'description'   : 'install llvm-gcc',
                                        'haltOnFailure' : True },]),
         'category'  : 'llvm-gcc' },

        {'name'      : "llvm-gcc-i686-pc-linux-gnu-cross-arm-eabi-hard-float",
         'slavenames': [ "kistanova4" ],
         'builddir'  : "llvm-gcc-i686-pc-linux-gnu-cross-arm-eabi-hard-float",
         'factory'   : ScriptedBuilder.getScriptedBuildFactory(
                       source_code  = [SVN(name='svn-llvm',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm/',
                                           defaultBranch='trunk',
                                           workdir="llvm.src"),
                                       SVN(name='svn-llvm-gcc',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm-gcc-4.2/',
                                           defaultBranch='trunk',
                                           workdir="llvm-gcc.src"),],
                       launcher     = 'llvm-gcc.src/extras/buildbot-launcher',
                       build_script = 'llvm-gcc.src/extras/build-x-4-armeabi-hardfloat',
                       extra_args   = [],
                       build_steps  = [{'name'          : 'clean',
                                        'description'   : 'clean',
                                        'haltOnFailure' : True },
                                       {'name'          : 'copy_cross_tools',
                                        'description'   : 'copy cross-tools',
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvm',
                                        'description'   : 'configure llvm',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvm',
                                        'description'   : 'make llvm',
                                        'extra_args'    : ['-j4'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvm',
                                        'description'   : 'install llvm',
                                        'extra_args'    : ['-j4'],
                                        'haltOnFailure' : False },
                                       {'name'          : 'configure_llvmgcc',
                                        'description'   : 'configure llvm-gcc',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvmgcc',
                                        'description'   : 'make llvm-gcc',
                                        'extra_args'    : ['-j4'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvmgcc',
                                        'description'   : 'install llvm-gcc',
                                        'haltOnFailure' : True },]),
         'category'  : 'llvm-gcc' },

        {'name'      : "llvm-gcc-i686-pc-linux-gnu-cross-arm-eabi-soft-float",
         'slavenames': [ "kistanova4" ],
         'builddir'  : "llvm-gcc-i686-pc-linux-gnu-cross-arm-eabi-soft-float",
         'factory'   : ScriptedBuilder.getScriptedBuildFactory(
                       source_code  = [SVN(name='svn-llvm',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm/',
                                           defaultBranch='trunk',
                                           workdir="llvm.src"),
                                       SVN(name='svn-llvm-gcc',
                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm-gcc-4.2/',
                                           defaultBranch='trunk',
                                           workdir="llvm-gcc.src"),],
                       launcher     = 'llvm-gcc.src/extras/buildbot-launcher',
                       build_script = 'llvm-gcc.src/extras/build-x-4-armeabi-softfloat',
                       extra_args   = [],
                       build_steps  = [{'name'          : 'clean',
                                        'description'   : 'clean',
                                        'haltOnFailure' : True },
                                       {'name'          : 'copy_cross_tools',
                                        'description'   : 'copy cross-tools',
                                        'haltOnFailure' : True },
                                       {'name'          : 'configure_llvm',
                                        'description'   : 'configure llvm',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvm',
                                        'description'   : 'make llvm',
                                        'extra_args'    : ['-j4'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvm',
                                        'description'   : 'install llvm',
                                        'extra_args'    : ['-j4'],
                                        'haltOnFailure' : False },
                                       {'name'          : 'configure_llvmgcc',
                                        'description'   : 'configure llvm-gcc',
                                        'haltOnFailure' : True },
                                       {'name'          : 'make_llvmgcc',
                                        'description'   : 'make llvm-gcc',
                                        'extra_args'    : ['-j4'],
                                        'haltOnFailure' : True },
                                       {'name'          : 'install_llvmgcc',
                                        'description'   : 'install llvm-gcc',
                                        'haltOnFailure' : True },]),
         'category'  : 'llvm-gcc' },

#        {'name'      : "llvm-gcc-mingw32-cross-arm-linux-gnueabi-hard-float",
#         'slavenames': [ "kistanova5" ],
#         'builddir'  : "llvm-gcc-mingw32-cross-arm-linux-gnueabi-hard-float",
#         'factory'   : ScriptedBuilder.getScriptedBuildFactory(
#                       source_code  = [SVN(name='svn-llvm',
#                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm/',
#                                           defaultBranch='trunk',
#                                           workdir="llvm.src"),
#                                       SVN(name='svn-llvm-gcc',
#                                           mode='update', baseURL='http://llvm.org/svn/llvm-project/llvm-gcc-4.2/',
#                                           defaultBranch='trunk',
#                                           workdir="llvm-gcc.src"),],
#                       launcher     = 'llvm-gcc.src/extras/buildbot-launcher',
#                       build_script = 'llvm-gcc.src/extras/llvm-gcc-mingw32-cross-arm-linux-gnueabi-hard-float',
#                       extra_args   = [],
#                       build_steps  = [{'name'          : 'clean',
#                                        'description'   : 'clean',
#                                        'haltOnFailure' : True },
#                                       {'name'          : 'copy_cross_tools',
#                                        'description'   : 'copy cross-tools',
#                                        'haltOnFailure' : True },
#                                       {'name'          : 'configure_llvm',
#                                        'description'   : 'configure llvm',
#                                        'haltOnFailure' : True },
#                                       {'name'          : 'make_llvm',
#                                        'description'   : 'make llvm',
#                                        'haltOnFailure' : True },
#                                       {'name'          : 'configure_llvmgcc',
#                                        'description'   : 'configure llvm-gcc',
#                                        'haltOnFailure' : True },
#                                       {'name'          : 'make_llvmgcc',
#                                        'description'   : 'make llvm-gcc',
#                                        'haltOnFailure' : True },
#                                       {'name'          : 'install_llvmgcc',
#                                        'description'   : 'install llvm-gcc',
#                                        'haltOnFailure' : True },]),
#         'category'  : 'llvm-gcc' },
#        {'name' : "clang-i686-xp-msvc9_alt",
#         'slavenames' :['adobe1'],
#         'builddir' :"clang-i686-xp-msvc9_alt",
#         'factory' : ClangBuilder.getClangMSVCBuildFactory(jobs=2),
#         'category' : 'clang.exp' },

        {'name': "clang-i686-freebsd-selfhost-rel",
         'slavenames':["freebsd1"],
         'builddir':"clang-i686-freebsd-selfhost-rel",
         'factory': ClangBuilder.getClangBuildFactory(triple='i686-pc-freebsd',
                                                      useTwoStage=True,
                                                      stage1_config='Release+Asserts',
                                                      stage2_config='Release+Asserts'),
         'category' : 'clang.exp' },

        ]

def get_builders():
    for b in _get_llvm_builders():
        b['category'] = 'llvm'
        yield b

    for b in _get_llvmgcc_builders():
        b['category'] = 'llvm-gcc'
        yield b

    for b in _get_dragonegg_builders():
        b['category'] = 'dragonegg'
        yield b

    for b in _get_clang_builders():
        b['category'] = 'clang'
        yield b

    for b in _get_polly_builders():
        b['category'] = 'polly'
        yield b

    for b in _get_lldb_builders():
        b['category'] = 'lldb'
        yield b

    for b in _get_experimental_builders():
        yield b

# Random other unused builders...

{'name': "clang-x86_64-openbsd",
 'slavenames':["ocean1"],
 'builddir':"clang-x86_64-openbsd",
 'factory': ClangBuilder.getClangBuildFactory(),
 'category':'clang.exp'}

