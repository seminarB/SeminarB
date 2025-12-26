import ast
import os
import shutil
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


# class ClassCollector(ast.NodeVisitor):
#     def __init__(self):
#         self.classes = []  # ast.ClassDef

#     def visit_ClassDef(self, node):
#         self.classes.append(node)
#         # class 内部はここでは深掘りしない

# def split_class(cls: ast.ClassDef, base_dir="tmp"):
#     class_dir = os.path.join(base_dir, cls.name)
#     os.mkdir(class_dir)

#     methods = []
#     others = []

#     for stmt in cls.body:
#         if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
#             methods.append(stmt)
#         else:
#             others.append(stmt)

#     # class 内関数
#     for fn in methods:
#         remove_inner_functions(fn)
#         code = ast.unparse(fn)
#         with open(f"{class_dir}/{fn.name}.py", "w") as f:
#             f.write(code)

#     # class 内 source_other
#     if others:
#         mod = ast.Module(body=others, type_ignores=[])
#         code = ast.unparse(mod)
#         with open(f"{class_dir}/source_other.py", "w") as f:
#             f.write(code)


def remove_inner_functions(fn):
    fn.body = [
        n for n in fn.body
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

class RemoveNestedFunctions(ast.NodeTransformer):
    def __init__(self):
        self.depth = 0

    def visit_FunctionDef(self, node):
        self.depth += 1

        if self.depth > 1:
            # ネスト関数自身は残す（切り出し用）
            return node

        # トップレベル関数の場合だけ body を加工
        node.body = [
            stmt for stmt in node.body
            if not isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        self.generic_visit(node)
        self.depth -= 1
        return node

    def visit_AsyncFunctionDef(self, node):
        return self.visit_FunctionDef(node)

def split_functions(src_path):
    with open(src_path, "r") as f:
        src = f.read()

    tree = ast.parse(src)

    # tree = RemoveNestedFunctions().visit(tree)
    # ast.fix_missing_locations(tree)

    collector = FunctionCollector()
    collector.visit(tree)

    target_dir = 'tmp'

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)

    function_names = []

    for fn, parent in collector.functions:
        remove_inner_functions(fn)
        name = fn.name
        function_names.append(name)

        code = ast.unparse(fn)
        with open(f"tmp/{name}.py", "w") as f:
            f.write(code)

    others = [
        node for node in tree.body
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]


    if others:
        mod = ast.Module(body=others, type_ignores=[])
        code = ast.unparse(mod)
        with open("tmp/source_other.py", "w") as f:
            f.write(code + "\n")
    function_names.append("source_other")
    return function_names

# def split_functions(src_path):
#     with open(src_path, "r") as f:
#         src = f.read()

#     tree = ast.parse(src)

#     target_dir = 'tmp'
#     if os.path.exists(target_dir):
#         shutil.rmtree(target_dir)
#     os.mkdir(target_dir)

#     # --- class 処理 ---
#     class_collector = ClassCollector()
#     class_collector.visit(tree)

#     for cls in class_collector.classes:
#         split_class(cls, target_dir)

#     # --- トップレベル関数 ---
#     func_collector = FunctionCollector()
#     func_collector.visit(tree)

#     function_names = []

#     for fn, parent in func_collector.functions:
#         if parent is not None:
#             continue  # class 内関数は除外

#         remove_inner_functions(fn)
#         function_names.append(fn.name)

#         code = ast.unparse(fn)
#         with open(f"tmp/{fn.name}.py", "w") as f:
#             f.write(code)

#     # --- トップレベル source_other ---
#     others = [
#         node for node in tree.body
#         if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
#     ]

#     if others:
#         mod = ast.Module(body=others, type_ignores=[])
#         code = ast.unparse(mod)
#         with open("tmp/source_other.py", "w") as f:
#             f.write(code)

#     function_names.append("source_other")
#     return function_names


def count_code_lines(func):
    with open(f"tmp/{func}.py", "rb") as f:
        tokens = tokenize.tokenize(f.readline)

        code_lines = set()

        for tok in tokens:
            tokentype = tok.type
            srow = tok.start[0]

            if tokentype in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.ENCODING, tokenize.ENDMARKER, tokenize.STRING, tokenize.INDENT, tokenize.DEDENT):
                continue

            code_lines.add(srow)

    return len(code_lines)

def main(filename):
    NG_FUNC = []
    funcs = split_functions(filename)
    for func in funcs:
        with open(f"tmp/{func}.py", "r") as f:
            src = f.read()
        line = count_code_lines(func)

        tree = ast.parse(src)
        counter = ConditionCounter()
        counter.visit(tree)
        branch_count = sum(counter.conds.values())
        depth = counter.max_depth
        branch_count_threshhold = 4
        depth_threshhold = 2
        line_threshhold = 50
        if branch_count > branch_count or depth > depth_threshhold or line > line_threshhold:
            NG_FUNC.append(func)
        print(f"{func}: {branch_count}: Max Depth={depth}: Lines={line}")
    return NG_FUNC

if __name__ == '__main__':
    main("analyze.py")