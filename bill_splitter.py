import re

print("Restaurant Bill Splitter for Lazy People")
print("(Food Item/Subtotal) * Grand Total")
print("* Please format as just numbers w/o the '$'* ")
print("========================================")

SALES_TAX = 0.1025
subtotal = 0
grand_total = 0
items = 0
operators = {'+', '-', '*', '/'}
priority = {'+': 1, '-': 1, '*': 2, '/': 2} 

# Checks for float
def is_float(value):
    try:
        v = float(value)
        return True
    except ValueError:
        return False

# Splits the expression by math operator tokens
def expression_split(expression):
    pattern = re.compile(r'(\d+\.\d+|\d+|\+|\-|\*|\/|\(|\))')
    return pattern.findall(expression)

# Performs the mathematical operation
def perform_operation(operator, op1, op2):
    if operator == '+':
        return op1 + op2
    elif operator == '-':
        return op1 - op2
    elif operator == '*':
        return op1 * op2
    elif operator == '/':
        return op1 / op2
    else:
        raise ValueError(f'=== Unsupported operator: {operator} ===')

# Evaluates expression w/ GEMDAS rules
def evaluate(tokens):
    stack = []
    try:
        for token in tokens:
            if is_float(token) or (token[0] == '-' and token[1:].isdigit()):
                stack.append(float(token))
            elif token in operators:
                while stack and stack[-1] in operators and priority[token] <= priority[stack[-1]]:
                    op2 = stack.pop()
                    operator = stack.pop()
                    op1 = stack.pop()
                    stack.append(perform_operation(operator, op1, op2))
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                result = 0
                while stack and stack[-1] != '(':
                    op2 = stack.pop()
                    operator = stack.pop()
                    op1 = stack.pop()
                    result = perform_operation(operator, op1, op2)
                stack.pop()  
                stack.append(result)
        
        while len(stack) > 1:
            op2 = stack.pop()
            operator = stack.pop()
            op1 = stack.pop()
            stack.append(perform_operation(operator, op1, op2))

        return stack.pop()
    except:
        raise SyntaxError(f'=== Error Parsing Expression ===')


while (True):
    try:
        subtotal = float(input("What was the subtotal? (Cost w/o Tip): "))
        grand_total = float(input("What was the grand total? (Cost w/ Tip): "))
        items = int(input("How many items were there?: "))
    except ValueError:
        print("*Please enter a valid number for your responses!*")
        continue
    else:
        break

print("\n======================")
print("** EXPRESSIONS ACCEPTED [+,-,*,/] **")
print("** Evaluated left -> right (NOT GEMDAS) **")
print("** Ex: 5.0 + 2.0 * 7")
print("======================\n")
counter = 0;
while counter < items:
    while (True):
        try: 
            split_expression = expression_split(input(f'Cost of Item #{counter + 1}: ').replace(" ", ""))
            item_cost = evaluate(split_expression)
            result = round((item_cost * (1 + SALES_TAX)) / subtotal * grand_total, 2)
            print(f'* Item #{counter + 1}: {result} *\n')

            counter = counter + 1
            break;
        except ValueError:
            print("*Please enter a valid number for your responses!*")
            continue