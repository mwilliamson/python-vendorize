import ast
import collections


def rewrite_imports_in_module(source, top_level_names, depth):
    source_lines = source.splitlines(True)
    
    def _should_rewrite_import(name):
        return name.split(".")[0] in top_level_names
    
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
            for name_index, name in enumerate(node.names):
                if _should_rewrite_import(name.name):
                    raise Exception("import rewriting not implemented")
            
        def visit_ImportFrom(self, node):
            if _should_rewrite_import(node.module):
                replacements.append(_generate_import_from_replacement(node))
    
    python_ast = ast.parse(source)
    ImportVisitor().visit(python_ast)
    return _replace_strings(source, replacements)


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


