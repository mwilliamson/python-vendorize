from __future__ import unicode_literals

from nose.tools import istest, assert_equal

from vendorize.import_rewrite import rewrite_imports_in_module


@istest
def module_without_imports_is_unchanged():
    assert_equal(
        "print(42)",
        rewrite_imports_in_module(
            "print(42)",
            top_level_names=[],
            depth=0))


@istest
def absolute_from_import_is_unchanged_if_not_in_set_of_names_to_change():
    assert_equal(
        "from b import c",
        rewrite_imports_in_module(
            "from b import c",
            top_level_names=["a"],
            depth=0))


@istest
def absolute_from_import_is_rewritten_to_relative_import():
    assert_equal(
        "from .a import b",
        rewrite_imports_in_module(
            "from a import b",
            top_level_names=["a"],
            depth=0))


@istest
def absolute_from_import_is_rewritten_to_relative_import_according_to_depth():
    assert_equal(
        "from ...a import b",
        rewrite_imports_in_module(
            "from a import b",
            top_level_names=["a"],
            depth=2))

@istest
def absolute_from_import_is_rewritten_to_relative_import_according_to_depth():
    assert_equal(
        "from ...a import b",
        rewrite_imports_in_module(
            "from a import b",
            top_level_names=["a"],
            depth=2))

@istest
def relative_from_import_is_ignored():
    assert_equal(
        "from . import b",
        rewrite_imports_in_module(
            "from . import b",
            top_level_names=["a"],
            depth=2))

@istest
def absolute_simple_import_of_top_level_module_is_rewritten_to_relative_import():
    assert_equal(
        "from ... import a",
        rewrite_imports_in_module(
            "import a",
            top_level_names=["a"],
            depth=2))

@istest
def absolute_simple_aliased_import_of_top_level_module_is_rewritten_to_relative_import():
    assert_equal(
        "from ... import a as b",
        rewrite_imports_in_module(
            "import a as b",
            top_level_names=["a"],
            depth=2))

@istest
def absolute_simple_aliased_import_of_submodule_is_rewritten_to_relative_import():
    assert_equal(
        "from ...a import b as c",
        rewrite_imports_in_module(
            "import a.b as c",
            top_level_names=["a"],
            depth=2))

@istest
def absolute_simple_import_of_submodule_is_rewritten_to_relative_import():
    assert_equal(
        "from ... import a\nfrom ...a import b as ___vendorize__0\na.b = ___vendorize__0",
        rewrite_imports_in_module(
            "import a.b",
            top_level_names=["a"],
            depth=2))

@istest
def can_have_single_import_statement_that_uses_both_rewritten_and_unrewritten_imports():
    assert_equal(
        "from ... import a\nimport b",
        rewrite_imports_in_module(
            "import a, b",
            top_level_names=["a"],
            depth=2))
