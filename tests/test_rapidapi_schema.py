"""Test the converters without importing optional model/GPU dependencies."""
import ast
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_converters():
    # Compile the real normalization functions and conversion methods in isolation:
    # importing the inference modules would also load all model backends.
    utils = ast.parse((ROOT / "toolbench/utils.py").read_text(encoding="utf-8"))
    functions = [node for node in utils.body if isinstance(node, ast.FunctionDef)
                 and node.name in {"standardize", "change_name"}]
    namespace = {"re": re}
    exec(compile(ast.Module(body=functions, type_ignores=[]), "utils.py", "exec"), namespace)
    converters = {}
    for filename in ("rapidapi.py", "rapidapi_multithread.py"):
        path = ROOT / "toolbench/inference/Downstream_tasks" / filename
        tree = ast.parse(path.read_text(encoding="utf-8"))
        wrapper = next(node for node in tree.body if isinstance(node, ast.ClassDef)
                       and node.name == "rapidapi_wrapper")
        method = next(node for node in wrapper.body if isinstance(node, ast.FunctionDef)
                      and node.name == "api_json_to_openai_json")
        scope = namespace.copy()
        exec(compile(ast.Module(body=[method], type_ignores=[]), str(path), "exec"), scope)
        converters[filename] = scope[method.name]
    return converters


def parameter(name, kind="STRING", default="", description="A parameter"):
    return {"name": name, "type": kind, "default": default, "description": description}


class RapidAPISchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.converters = load_converters()

    def check_schemas(self, fields, required, optional, properties):
        api = {"api_name": "Search items", "api_description": "Find items",
               "category_name": "Search", **fields}
        for filename, convert in self.converters.items():
            with self.subTest(converter=filename):
                result, category, api_name = convert(None, api, "example_tool")
                self.assertEqual((category, api_name), ("Search", "search_items"))
                self.assertEqual(result["function"]["name"], "search_items_for_example_tool")
                schema = result["function"]["parameters"]
                self.assertEqual(schema["properties"], properties)
                self.assertEqual(schema["required"], required)
                self.assertEqual(schema["optional"], optional)

    def test_optional_parameters_with_empty_required(self):
        self.check_schemas(
            {"required_parameters": [], "optional_parameters": [
                parameter("Page Number", "NUMBER", 0),
                parameter("Include Archived", "BOOLEAN", False),
                parameter("from", default="all", description="x" * 300)]},
            [], ["page_number", "include_archived", "is_from"],
            {"page_number": {"type": "integer", "description": "A parameter", "example_value": 0},
             "include_archived": {"type": "boolean", "description": "A parameter", "example_value": False},
             "is_from": {"type": "string", "description": "x" * 256, "example_value": "all"}})

    def test_optional_parameters_without_required_key(self):
        self.check_schemas({"optional_parameters": [parameter("query")]}, [], ["query"],
                           {"query": {"type": "string", "description": "A parameter"}})

    def test_mixed_parameters(self):
        self.check_schemas(
            {"required_parameters": [parameter("query")],
             "optional_parameters": [parameter("page", "NUMBER", 1)]},
            ["query"], ["page"],
            {"query": {"type": "string", "description": "A parameter"},
             "page": {"type": "integer", "description": "A parameter", "example_value": 1}})

    def test_required_only(self):
        self.check_schemas({"required_parameters": [parameter("query")], "optional_parameters": []},
                           ["query"], [], {"query": {"type": "string", "description": "A parameter"}})

    def test_required_only_without_optional_key(self):
        self.check_schemas({"required_parameters": [parameter("query")]}, ["query"], [],
                           {"query": {"type": "string", "description": "A parameter"}})

    def test_empty_parameters(self):
        self.check_schemas({"required_parameters": [], "optional_parameters": []}, [], [], {})

    def test_missing_parameter_keys(self):
        self.check_schemas({}, [], [], {})


if __name__ == "__main__":
    unittest.main()
