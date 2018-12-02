import io

from nose.tools import assert_equal

from vendorize.python_source import find_encoding


def test_empty_file_has_encoding_of_utf_8():
    assert_equal(
        "utf-8",
        find_encoding(io.BytesIO(b"")),
    )


def test_encoding_can_be_read_from_first_line():
    assert_equal(
        "latin-1",
        find_encoding(io.BytesIO(b"# encoding=latin-1")),
    )


def test_encoding_can_be_read_from_second_line():
    assert_equal(
        "latin-1",
        find_encoding(io.BytesIO(b"#!/usr/bin/env python\n# encoding=latin-1")),
    )


def test_encoding_cannot_be_read_after_third_line():
    assert_equal(
        "utf-8",
        find_encoding(io.BytesIO(b"\n\n# encoding=latin-1")),
    )
