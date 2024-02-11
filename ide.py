import subprocess,os, tkinter
import tkinter as tk
from tkinter import scrolledtext

def lexing1(var):
    tokken = ["Montrer"]
    s1 = list(var)

    i = 0
    while i < len(s1) - 2:
        if s1[i].isdigit() and  s1[i + 1]=="." and s1[i + 2].isdigit():
            k = i+2
            while s1[k].isdigit():
                k+=1
            s1[i] = "".join(s1[i:k])
            del s1[i + 1: k]
            i+=1

        else:
            i+=1

    for k in tokken:
        indexs1 = 0
        while indexs1 < len(s1):
            if k.endswith(s1[indexs1]) and indexs1 + 1 >= len(k):
                flag = all(k[e - 1] == s1[indexs1 - (len(k) - e)] for e in range(len(k), 0, -1))
                if flag:
                    s1[indexs1] = "".join(s1[indexs1 - len(k) + 1: indexs1 + 1])
                    del s1[indexs1 - len(k) + 1: indexs1]
                    indexs1 = 0
            indexs1 += 1

    indexs1 = 0
    while indexs1 < len(s1) - 1:
        if s1[indexs1] == '"':
            index0 = indexs1 + 1
            while s1[index0] != '"':
                index0 += 1
            s1[indexs1] = "".join(s1[indexs1: index0 + 1])
            del s1[indexs1 + 1: index0 + 1]
            indexs1 += 1

        indexs1 += 1

    for ins in reversed(s1):
        if ins == " ":
            s1.remove(ins)
    return s1

def display_tree(tree, depth=0, prefix=""):
    if isinstance(tree, list):
        print(" " * depth + prefix + f"{tree[0]}")
        for i, subtree in enumerate(tree[1:]):
            if i == len(tree) - 2:
                display_tree(subtree, depth + 1, " " * (depth + len(prefix)) + "└── ")
            else:
                display_tree(subtree, depth + 1, " " * (depth + len(prefix)) + "├── ")
    else:
        print(" " * depth + prefix + str(tree))


def infix_to_postfix(expression):
    prio = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    rep = []
    pile = []

    for token in expression:
        if token[0] == '"':
            rep.append(token)
        elif token.isdigit() or token.replace('.', '').isdigit():
            rep.append(token)
        elif token == '(':
            pile.append(token)
        elif token == ')':
            while pile and pile[-1] != '(':
                rep.append(pile.pop())
            pile.pop()
        else:
            while pile and prio.get(pile[-1], 0) >= prio.get(token, 0):
                rep.append(pile.pop())
            pile.append(token)

    while pile:
        rep.append(pile.pop())

    return rep

def postfix_to_tree(postfix_expression):
    stack = []

    for token in postfix_expression:
        if token[0] == '"':
            stack.append(token)
        elif token.isdigit() or token.replace('.', '').isdigit():
            stack.append(token)
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.append([token, operand1, operand2])

    return stack[0]

def parsing(var):
    tokken = ["Montrer"]
    
    if var[0] in tokken and var[1] == ":":
        i = 2
        try:
            while i < len(var) and var[i] != ".":
                i += 1
            expr = var[2:i]
            postfix_expression = infix_to_postfix(expr)
            expression_tree = postfix_to_tree(postfix_expression)
            return [var[0], expression_tree]
        except Exception as e:
            print(f"Erreur lors de l'analyse : {e}")
            return 2
    else:
        return 1




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



def run_code():
    output_text.delete(1.0, tk.END)
    error_text.delete(1.0, tk.END)
    try:
        var = code_text.get(1.0, tk.END)
        var = lexing1(var)
        res = parsing(var)
        display_tree(res)
        navigate(res, head, body)
        head.append("\n".join(body))

        head.append("return 0;\n}")
        with open("output.c", "w") as c_file:
            c_file.write("\n".join(head))
        c_file.close()

        subprocess.run(['gcc', 'output.c', '-o', 'srt'])
        process = subprocess.Popen('srt.exe', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        stdout, stderr = process.communicate()
        os.remove("srt.exe")
        os.remove("output.c")
        
    except Exception as e:
        error_text.insert(tk.END, f"Erreur : {str(e)}")
    
    output_result = stdout
    error_result = stderr
    output_text.insert(tk.END, output_result)
    error_text.insert(tk.END, error_result)

head = ["#include <stdio.h>\n\ndouble stack[100];\ndouble a;\ndouble b;\nint stack_top = -1;\n\nvoid stack_push(double value) {\n    stack[++stack_top] = value;\n}\n\ndouble stack_pop() {\n    return stack[stack_top--];\n}\n\nint main() {"]
body = []


root = tk.Tk()
root.title("Simple Code Runner")
code_text = scrolledtext.ScrolledText(root, width=40, height=20, wrap=tk.WORD)
code_text.pack(side=tk.LEFT, padx=10, pady=10)
run_button = tk.Button(root, text="Run Code", command=run_code)
run_button.pack(side=tk.TOP, pady=10)
output_text = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
output_text.pack(side=tk.TOP, padx=10, pady=10)
error_text = scrolledtext.ScrolledText(root, width=40, height=5, wrap=tk.WORD, fg="red")
error_text.pack(side=tk.TOP, padx=10, pady=10)
root.mainloop()




