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
        print(token)
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


var = ['Montrer', ':', '3', '+', '5.22545', '.']
result = parsing(var)
print(result)
display_tree(result)

