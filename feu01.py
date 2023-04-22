# Évaluer une expression

import sys


def priority(operator):
    if operator in '*/%':
        return 2
    elif operator in '+-':
        return 1
    else:
        return 0


def operation(a, op, b):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
    elif op == '%':
        return a % b


def string_calculator(arg):
    values = []
    operators = []
    number = ""

    for n in arg:
        if n.isdigit():
            number += n
        else:
            if number:
                values.append(int(number))
                number = ""
            if n == "(":
                operators.append(n)
            elif n in '+-*/%':
                while operators and priority(n) <= priority(operators[-1]):
                    op = operators.pop()
                    b = values.pop()
                    a = values.pop()
                    result = operation(a, op, b)
                    values.append(result)
                operators.append(n)
            elif n == ')':
                while operators and operators[-1] != '(':
                    op = operators.pop()
                    b = values.pop()
                    a = values.pop()
                    result = operation(a, op, b)
                    values.append(result)
                if operators and operators[-1] == '(':
                    operators.pop()
            elif n == " ":
                continue

    if number:
        values.append(int(number))

    while operators:
        op = operators.pop()
        b = values.pop()
        a = values.pop()

        result = operation(a, op, b)

        values.append(result)

    final_result = values[-1]
    print(final_result)


try:
    argument = sys.argv[1]
    string_calculator(argument)
except IndexError:
    print("error")
