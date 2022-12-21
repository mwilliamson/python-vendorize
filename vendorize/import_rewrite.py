import ast
import tokenize
import io
import collections
import itertools


def rewrite_imports_in_module(source, top_level_names, depth):
    source_lines = source.splitlines(True)
    line_endings = list(_find_line_endings(source))

    def _find_line_ending(position):
        for line_ending in line_endings:
            if line_ending >= position:
                return line_ending

        raise Exception("Could not find line ending")

    def _should_rewrite_import(name):
        return name.split(".")[0] in top_level_names

    def _generate_simple_import_replacement(node):
        temp_index = itertools.count()

        replacement = []

        for name in node.names:
            if _should_rewrite_import(name.name):
                parts = name.name.split(".")
                if name.asname is None:
                    replacement.append("from ." + ("." * depth) + " import " + parts[0])
                    variable_name = "___vendorize__{0}".format(next(temp_index))
                    if len(parts) > 1:
                        replacement.append(
                            "from ." + ("." * depth) + ".".join(parts[:-1]) +
                            " import " + parts[-1] +
                            " as " + variable_name
                        )
                else:
                    replacement.append(
                        "from ." + ("." * depth) + ".".join(parts[:-1]) +
                        " import " + parts[-1] +
                        " as " + name.asname)
            else:
                statement = "import " + name.name
                if name.asname is not None:
                    statement += " as " + name.asname
                replacement.append(statement)

        _, line_ending_col_offset = _find_line_ending((node.lineno, node.col_offset))
        return _Replacement(
            _Location(node.lineno, node.col_offset),
            # TODO: handle multi-line statements
            line_ending_col_offset - node.col_offset,
            ";".join(replacement))

    def _generate_import_from_replacement(node):
        line = source_lines[node.lineno - 1]
        col_offset = node.col_offset
        from_keyword = "from"
        assert line[col_offset:col_offset + len(from_keyword)] == from_keyword
        col_offset += len(from_keyword)
        while line[col_offset].isspace():
            col_offset += 1
        return _Replacement(
            _Location(node.lineno, col_offset),
            0,
            "." + ("." * depth))

    replacements = []

    class ImportVisitor(ast.NodeVisitor):
        def visit_Import(self, node):
            if any(_should_rewrite_import(name.name) for name in node.names):
                replacements.append(_generate_simple_import_replacement(node))

        def visit_ImportFrom(self, node):
            if not node.level and _should_rewrite_import(node.module):
                replacements.append(_generate_import_from_replacement(node))

    python_ast = ast.parse(source)
    ImportVisitor().visit(python_ast)
    return _replace_strings(source, replacements)


def _find_line_endings(source):
    token_stream = tokenize.generate_tokens(io.StringIO(source + "\n").readline)
    for token_type, token_str, start, end, line in token_stream:
        if token_type == tokenize.NEWLINE:
            yield start


_Location = collections.namedtuple("_Location", ["lineno", "col_offset"])

_Replacement = collections.namedtuple("_Replacement", [
    "location",
    "length",
    "value"
])

def _replace_strings(source, replacements):
    lines = source.splitlines(True)

    replacements = sorted(replacements, key=lambda replacement: replacement.location, reverse=True)

    for replacement in replacements:
        line_index = replacement.location.lineno - 1
        col_offset = replacement.location.col_offset
        lines[line_index] = _str_replace(lines[line_index], replacement.length, col_offset, replacement.value)

    return "".join(lines)


def _str_replace(original, length, index, to_insert):
    return original[:index] + to_insert + original[index + length:]


