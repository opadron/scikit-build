#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""test_hello_pure
----------------------------------

Tries to build and test the `hello-pure` sample project.
"""

import glob
import os

from skbuild.cmaker import SKBUILD_DIR
from skbuild.utils import push_dir

from . import project_setup_py_test


@project_setup_py_test(("samples", "hello-pure"), ["build"], clear_cache=True)
def test_hello_pure_builds(capsys):
    out, _ = capsys.readouterr()
    assert "skipping skbuild (no CMakeLists.txt found)" in out


# @project_setup_py_test(("samples", "hello-pure"), ["test"])
# def test_hello_cython_works():
#     pass


@project_setup_py_test(("samples", "hello-pure"), ["sdist"])
def test_hello_pure_sdist():
    sdists_tar = glob.glob('dist/*.tar.gz')
    sdists_zip = glob.glob('dist/*.zip')
    assert sdists_tar or sdists_zip


@project_setup_py_test(("samples", "hello-pure"), ["bdist_wheel"])
def test_hello_pure_wheel():
    whls = glob.glob('dist/*.whl')
    assert len(whls) == 1
    assert whls[0].endswith('-none-any.whl')


def test_hello_clean(capfd):
    with push_dir():

        skbuild_dir = os.path.join(
            "tests", "samples", "hello-pure", SKBUILD_DIR)

        @project_setup_py_test(("samples", "hello-pure"), ["build"],
                               clear_cache=True)
        def run_build():
            pass

        run_build()

        assert os.path.exists(skbuild_dir)

        @project_setup_py_test(("samples", "hello-pure"), ["clean"])
        def run_clean():
            pass

        run_clean()

        assert not os.path.exists(skbuild_dir)

        out = capfd.readouterr()[0]
        assert 'Build files have been written to' not in out
