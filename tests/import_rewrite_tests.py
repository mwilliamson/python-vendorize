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
