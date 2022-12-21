from vendorize.import_rewrite import rewrite_imports_in_module


def test_module_without_imports_is_unchanged():
    result = rewrite_imports_in_module(
        "print(42)",
        top_level_names=[],
        depth=0,
    )

    assert "print(42)" == result


def test_absolute_from_import_is_unchanged_if_not_in_set_of_names_to_change():
    result = rewrite_imports_in_module(
        "from b import c",
        top_level_names=["a"],
        depth=0,
    )

    assert "from b import c" == result


def test_absolute_from_import_is_rewritten_to_relative_import():
    result = rewrite_imports_in_module(
        "from a import b",
        top_level_names=["a"],
        depth=0,
    )

    assert "from .a import b" == result


def test_absolute_from_import_is_rewritten_to_relative_import_according_to_depth():
    result = rewrite_imports_in_module(
        "from a import b",
        top_level_names=["a"],
        depth=2,
    )

    assert "from ...a import b" == result


def test_absolute_from_import_is_rewritten_to_relative_import_according_to_depth():
    result = rewrite_imports_in_module(
        "from a import b",
        top_level_names=["a"],
        depth=2,
    )

    assert "from ...a import b" == result


def test_relative_from_import_is_ignored():
    result = rewrite_imports_in_module(
        "from . import b",
        top_level_names=["a"],
        depth=2,
    )

    assert "from . import b" == result


def test_absolute_simple_import_of_top_level_module_is_rewritten_to_relative_import():
    result = rewrite_imports_in_module(
        "import a",
        top_level_names=["a"],
        depth=2,
    )

    assert "from ... import a" == result


def test_absolute_simple_aliased_import_of_top_level_module_is_rewritten_to_relative_import():
    result = rewrite_imports_in_module(
        "import a as b",
        top_level_names=["a"],
        depth=2,
    )

    assert "from ... import a as b" == result


def test_absolute_simple_aliased_import_of_submodule_is_rewritten_to_relative_import():
    result = rewrite_imports_in_module(
        "import a.b as c",
        top_level_names=["a"],
        depth=2,
    )

    assert "from ...a import b as c" == result


def test_absolute_simple_import_of_submodule_is_rewritten_to_relative_import():
    result = rewrite_imports_in_module(
        "import a.b",
        top_level_names=["a"],
        depth=2,
    )

    assert "from ... import a;from ...a import b as ___vendorize__0" == result


def test_absolute_simple_import_of_nested_submodule_is_rewritten_to_relative_import():
    result = rewrite_imports_in_module(
        "import a.b.c.d",
        top_level_names=["a"],
        depth=2,
    )

    assert "from ... import a;from ...a.b.c import d as ___vendorize__0" == result


def test_can_have_single_import_statement_that_uses_both_rewritten_and_unrewritten_imports():
    result = rewrite_imports_in_module(
        "import a, b",
        top_level_names=["a"],
        depth=2,
    )

    assert "from ... import a;import b" == result
