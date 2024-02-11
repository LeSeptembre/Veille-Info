import subprocess
import os


def reacting_trad(act, head, body):
    ope = {'+': "+", '-': "-", '*': "*", '/': "/", '^': "pow"}
    tokken = ["Montrer"]

    if act.replace('.', '').isdigit() or (act[1:].replace('.', '').isdigit() and '.' in act):
        body.append(f"stack_push({act});")
    elif act in ope:
        body.append(f"if(stack_top >= 1) {{\n  a = stack_pop();\n  b = stack_pop();\n  stack_push(a {ope[act]} b);\n}} else {{\n  // Gérer le cas où la pile est vide\n}}")
    if act[0] == '"' and act[-1] == '"':
        str_value = act[1:-1]
        body.append(f'printf("{str_value}\\n");')
    elif act[0] == "'" and act[-1] == "'":
        char_value = ord(act[1])
        body.append(f'printf("%c\\n", {char_value});')

    if act in tokken:
        if act == "Montrer":
            body.append("if(stack_top >= 0) {\n  double value_to_print = stack_pop();\n  printf(\"%g\\n\", value_to_print);\n} else {\n  return 0;\n}")

def navigate(tree, head, body):
    if isinstance(tree, list):
        for i in range(len(tree) - 1, -1, -1):
            navigate(tree[i], head, body)
    else:
        reacting_trad(tree, head, body)

head = ["#include <stdio.h>\n\ndouble stack[100];\ndouble a;\ndouble b;\nint stack_top = -1;\n\nvoid stack_push(double value) {\n    stack[++stack_top] = value;\n}\n\ndouble stack_pop() {\n    return stack[stack_top--];\n}\n\nint main() {"]
body = []

res = ['Montrer',  '+', ['2.5','5']]
navigate(res, head, body)
head.append("\n".join(body))
head.append("return 0;\n}")

with open("output.c", "w") as c_file:
    c_file.write("\n".join(head))

subprocess.run(['gcc', 'output.c', '-o', 'srt'])
process = subprocess.Popen('srt.exe', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
stdout, stderr = process.communicate()

print("Sortie standard :\n", stdout)
print("Sortie d'erreur :\n", stderr)
os.remove("srt.exe")
