import os
import collections
import subprocess
import ast
from ._vendor.six.moves.configparser import RawConfigParser

from .files import mkdir_p, ensure_file_exists


def vendorize_requirements(path):
    require_prefix = "require:"
    parser = RawConfigParser()
    parser.read(path)
    target_directory = os.path.join(os.path.dirname(path), parser.get("vendorize", "target"))
    ensure_file_exists(os.path.join(target_directory, "__init__.py"))
    for section in parser.sections():
        if section.startswith(require_prefix):
            requirement = section[len(require_prefix):]
            vendorize_requirement(
                cwd=os.path.dirname(path) or None,
                requirement=requirement,
                target_directory=target_directory)


def vendorize_requirement(cwd, requirement, target_directory):
    mkdir_p(target_directory)
    subprocess.check_call(
        ["pip", "install", "--no-dependencies", "--target", target_directory, requirement],
        cwd=cwd)
    top_level_names = _read_top_level_names(target_directory)
    _rewrite_imports(target_directory, top_level_names)

def _read_top_level_names(target_directory):
    for name in os.listdir(target_directory):
        if name.endswith(".egg-info") or name.endswith(".dist-info"):
            path = os.path.join(target_directory, name, "top_level.txt")
            if os.path.exists(path):
                with open(path) as top_level_file:
                    return list(filter(None, map(lambda line: line.strip(), top_level_file)))
    
    raise Exception("Could not find top_level.txt")
            
def _rewrite_imports(target_directory, top_level_names):
    for top_level_name in top_level_names:
        module_path = os.path.join(target_directory, top_level_name + ".py")
        if os.path.exists(module_path):
            _rewrite_imports_in_module(module_path, top_level_names, depth=0)
        
        package_path = os.path.join(target_directory, top_level_name)
        if os.path.exists(package_path):
            _rewrite_imports_in_package(package_path, top_level_names, depth=1)

def _rewrite_imports_in_package(package_path, top_level_names, depth):
    for name in os.listdir(package_path):
        child_path = os.path.join(package_path, name)
        if name.endswith(".py"):
            _rewrite_imports_in_module(child_path, top_level_names, depth=depth)
        
        if os.path.isdir(child_path):
            _rewrite_imports_in_package(child_path, top_level_names, depth=depth + 1)
    
    
def _rewrite_imports_in_module(module_path, top_level_names, depth):
    with open(module_path) as source_file:
        source = source_file.read()
    
    with open(module_path) as source_file:
        source_lines = list(source_file)
    
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
    _replace_strings(module_path, replacements)


_Location = collections.namedtuple("_Location", ["lineno", "col_offset"])

_Replacement = collections.namedtuple("_Replacement", [
    "location",
    "length",
    "value"
])

def _replace_strings(path, replacements):
    with open(path) as source_file:
        lines = list(source_file.readlines())
    
    replacements = sorted(replacements, key=lambda replacement: replacement.location, reverse=True)
    
    for replacement in replacements:
        line_index = replacement.location.lineno - 1
        col_offset = replacement.location.col_offset
        lines[line_index] = _str_replace(lines[line_index], replacement.length, col_offset, replacement.value)
    
    with open(path, "w") as source_file:
        source_file.write("".join(lines))


def _str_replace(original, length, index, to_insert):
    return original[:index] + to_insert + original[index + length:]

