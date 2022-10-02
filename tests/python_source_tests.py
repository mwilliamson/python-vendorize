import io

from vendorize.python_source import find_encoding


def test_empty_file_has_encoding_of_utf_8():
    result = find_encoding(io.BytesIO(b""))

    assert "utf-8" == result


def test_encoding_can_be_read_from_first_line():
    result = find_encoding(io.BytesIO(b"# encoding=latin-1"))

    assert "latin-1" == result


def test_encoding_can_be_read_from_second_line():
    result = find_encoding(io.BytesIO(b"#!/usr/bin/env python\n# encoding=latin-1"))

    assert "latin-1" == result


def test_encoding_cannot_be_read_after_third_line():
    result = find_encoding(io.BytesIO(b"\n\n# encoding=latin-1"))

    assert "utf-8" == result
