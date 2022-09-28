import re
import sys
import os
import ast


def ast_check(file_name, line):
    tree = ast.parse(line)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [(a.arg, a.lineno) for a in node.args.args]
            for i in args:
                if re.match(r'[a-z]*[A-Z]+', i[0]):
                    print(f"{file_name}: Line {i[1]}: S010 Argument name '{i[0]}' should use snake_case")

        if isinstance(node, ast.FunctionDef):
            for n in node.body:
                if isinstance(n, ast.Assign):
                    for i in n.targets:
                        if isinstance(i, ast.Name):
                            if isinstance(i.ctx, ast.Store):
                                word = i.id
                                num = i.lineno
                                if re.match(r'[a-z]*[A-Z]+', word):
                                    print(f"{file_name}: Line {num}: S011 Variable '{word}' should use snake_case")

        if isinstance(node, ast.FunctionDef):
            for item in node.args.defaults:
                if isinstance(item, ast.List):
                    num = item.lineno
                    print(f"{file_name}: Line {num}: S012 Default argument value is mutable")


def check(file_name):

    with open(file_name) as f:
        st = 0
        for num, line in enumerate(f.readlines(), start=1):

            if not line.strip():
                st += 1
            elif line.strip() and st <= 2:
                st = 0

            if len(line) > 79:
                print(f'{file_name}: Line {num}: S001 Too long')

            if line.strip() and re.match(r'^\s+', line):
                if len(re.match(r'^\s+', line).group()) % 4:
                    print(f'{file_name}: Line {num}: S002 Indentation is not a multiple of four')

            if re.search(r';', line):
                if re.search(r'[\'\"].*;.*[\'\"]', line) or re.search(r'#.*;', line):
                    continue
                print(f'{file_name}: Line {num}: S003 Unnecessary semicolon')

            if re.search(r'.+#', line):
                if not re.search(r'\s{2}#', line):
                    print(f'{file_name}: Line {num}: S004 At least two spaces required before inline comments')

            if re.search(r'#.*todo', line, flags=re.IGNORECASE):
                print(f'{file_name}: Line {num}: S005 TODO found')

            if line.strip() and st > 2:
                print(f'{file_name}: Line {num}: S006 More than two blank lines used before this line')
                st = 0

            if re.search(r'(class|def)\s{2}', line):
                print(f"{file_name}: Line {num}: S007 Too many spaces after 'class'")

            if re.search(r'class\s[a-z]', line):
                name = re.search(r'class\s[a-z].+', line).group()[:-1].split()[1]
                print(f"{file_name}: Line {num}: S008 Class name '{name}' should use CamelCase")

            if re.search(r'def\s[a-z]*[A-Z]+', line):
                name = re.search(r'def\s[a-z]*[A-Z]+.+', line).group()[:-3].split()[1]
                print(f"{file_name}: Line {num}: S009 Function name '{name}' should use snake_case")

        f.seek(0)
        ast_check(file_name, f.read())


def main():
    args = sys.argv
    file_name = args[1]

    if os.path.isdir(file_name):
        files = os.listdir(file_name)
        for file in sorted(files):
            check(os.path.join(file_name, file))

    elif os.path.isfile(file_name):
        check(file_name)


if __name__ == "__main__":
    main()
