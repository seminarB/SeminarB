import ast
import os
import io
import copy
import tokenize

class ConditionCounter(ast.NodeVisitor):
    def __init__(self):
        self.conds = {
            "if": 0,
            "for": 0,
            "while": 0,
            "match": 0
        }
        self.depth = 0
        self.max_depth = 0

    def _enter(self):
        self.depth += 1
        self.max_depth = max(self.max_depth, self.depth)

    def _exit(self):
        self.depth -= 1

    def visit_If(self, node):
        self.conds["if"] += self._count_expr(node.test)

        if node.orelse and not isinstance(node.orelse[0], ast.If):
            self.conds["if"] += 1

        self._enter()
        self.generic_visit(node)
        self._exit()

    def visit_For(self, node):
        self.conds["for"] += 1
        self._enter()
        self.generic_visit(node)
        self._exit()

    def visit_While(self, node):
        self.conds["while"] += self._count_expr(node.test)
        self._enter()
        self.generic_visit(node)
        self._exit()

    def visit_Match(self, node):
        self.conds["match"] += len(node.cases)
        self._enter()
        self.generic_visit(node)
        self._exit()

    def _count_expr(self, expr):
        if isinstance(expr, ast.BoolOp):
            return sum(self._count_expr(v) for v in expr.values)

        if isinstance(expr, ast.UnaryOp):
            return self._count_expr(expr.operand)

        if isinstance(expr, ast.Compare):
            return 1

        if isinstance(expr, ast.Name):
            return 1

        return 1

class FunctionCollector(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.stack = []

    def visit_ClassDef(self, node):
        self.stack.append(node)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node):
        parent = self.stack[-1] if self.stack else None
        self.functions.append((node, parent))

        self.stack.append(node)
        self.generic_visit(node)
        self.stack.pop()

    def visit_AsyncFunctionDef(self, node):
        parent = self.stack[-1] if self.stack else None
        self.functions.append((node, parent))

        self.stack.append(node)
        self.generic_visit(node)
        self.stack.pop()

class RemoveNestedFunctions(ast.NodeTransformer):
    def __init__(self):
        self.depth = 0

    def visit_FunctionDef(self, node):
        self.depth += 1

        if self.depth > 1:
            return node

        node.body = [
            stmt for stmt in node.body
            if not isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        self.generic_visit(node)
        self.depth -= 1
        return node

    def visit_AsyncFunctionDef(self, node):
        return self.visit_FunctionDef(node)

def remove_inner_functions(fn):
    fn.body = [
        n for n in fn.body
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

# def split_functions(src):
#     tree = ast.parse(src)

#     collector = FunctionCollector()
#     collector.visit(tree)

#     functions = {}

#     for fn, parent in collector.functions:
#         remove_inner_functions(fn)
#         name = fn.name
#         functions[name] = {
#             "src": ast.unparse(fn),
#             "line": fn.lineno
#         }

#     # others = [
#     #     node for node in tree.body
#     #     if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
#     # ]

#     # if others:
#     #     mod = ast.Module(body=others, type_ignores=[])
#     #     functions["source_other"] = {
#     #         "src": ast.unparse(mod),
#     #         "line": 0
#     #     }

#     return functions

def split_functions(src):
    tree = ast.parse(src)

    collector = FunctionCollector()
    collector.visit(tree)

    functions = {}

    for fn, parent in collector.functions:
        name = fn.name

        # ① オリジナル（inner削除なし）
        original_fn = copy.deepcopy(fn)

        # ② 解析用（inner削除あり）
        analyzed_fn = copy.deepcopy(fn)
        remove_inner_functions(analyzed_fn)

        functions[name] = {
            "src": ast.unparse(analyzed_fn),
            "original_src": ast.unparse(original_fn),
            "line": fn.lineno
        }

    return functions

def count_code_lines_from_src(src):
    reader = io.StringIO(src)

    code_lines = set()
    tokens = tokenize.generate_tokens(reader.readline)
    for tok in tokens:
        if tok.type in (
            tokenize.COMMENT,
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.ENCODING,
            tokenize.ENDMARKER,
            tokenize.STRING,
            tokenize.INDENT,
            tokenize.DEDENT,
        ):
            continue

        code_lines.add(tok.start[0])

    return len(code_lines)

def main(src):
    NG_FUNC = {}

    funcs = split_functions(src)

    for name, info in funcs.items():
        func_src = info["src"]
        lineno = info["line"]

        line = count_code_lines_from_src(func_src)

        tree = ast.parse(func_src)
        counter = ConditionCounter()
        counter.visit(tree)

        branch_count = sum(counter.conds.values())
        depth = counter.max_depth

        branch_count_threshhold = 4
        depth_threshhold = 2
        line_threshhold = 50

        # branch_count_threshhold = 0
        # depth_threshhold = 0
        # line_threshhold = 0

        if (
            branch_count > branch_count_threshhold
            or depth > depth_threshhold
            or line > line_threshhold
        ):
            NG_FUNC[name] = {
                "src": func_src,
                "original_src" : info["original_src"],
                "line": lineno
            }

        # print(f"{name}: {branch_count}: Max Depth={depth}: Lines={line}")

    return NG_FUNC

if __name__ == '__main__':
    with open("analyze.py", "r") as f:
        src = f.read()
    # print(main(src))
    ng = main(src)

    for name, info in ng.items():
        print("----")
        print(f"NG FUNCTION: {name}")
        print(f"Defined at line: {info['line']}")
        print(info["original_src"])