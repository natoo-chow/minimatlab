import sympy as sp
import re
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
symbols_dict = {}
expressions_dict = {}

def print_help_info():
    help_text = """
===== Mini Matlab Symbolic Calculation System (Based on SymPy) =====
Common Commands (Case Insensitive):
1.  sym <variable names>          - Define symbolic variables (separate with spaces, e.g.: sym x y z)
2.  f <expr name> = <expression> - Define symbolic expression (e.g.: f f1 = x**2 + sin(x))
3.  show                         - View all defined symbolic variables and expressions
4.  simplify <expr name>         - Simplify the specified expression
5.  expand <expr name>           - Expand the specified expression (polynomial/trigonometric etc.)
6.  factor <expr name>           - Factor the specified polynomial expression
7.  diff <expr name> <var> [order] - Differentiate (1st order by default, e.g.: diff f1 x 2)
8.  int <expr name> <var> [lower upper] - Integrate (indefinite/definite, e.g.: int f1 x 0 1)
9.  limit <expr name> <var> <point> [direction] - Calculate limit (direction +/- , e.g.: limit f1 x 0 -)
10. solve <equation> <var>       - Solve equation (e.g.: solve x**2-4=0 x)
11. latex <expr name>            - Output LaTeX format of the expression
12. clear                        - Clear all symbolic variables and expressions
13. help                         - View help information
14. exit/quit                    - Exit the program
=============================================
"""
    print(help_text)

def handle_sym(cmd):
    try:
        var_names = re.sub(r'^sym\s*', '', cmd, flags=re.I).strip().split()
        if not var_names:
            print("Error: Please specify symbolic variable names, e.g.: sym x y")
            return
        for var in var_names:
            if var in symbols_dict:
                print(f"Tip: Variable '{var}' already exists")
                continue
            sym = sp.Symbol(var)
            symbols_dict[var] = sym
            globals()[var] = sym
        print(f"Successfully defined symbolic variables: {', '.join(var_names)}")
    except Exception as e:
        print(f"Failed to define variables: {e}")

def handle_f(cmd):
    try:
        pattern = r'f\s*(\w+)\s*=\s*(.+)'
        match = re.match(pattern, cmd, flags=re.I | re.DOTALL)
        if not match:
            print("Error: Invalid format, correct format: f <expr name> = <expression>, e.g.: f f1 = x**2")
            return
        expr_name, expr_str = match.groups()
        expr_name = expr_name.strip()
        expr_str = expr_str.strip()

        if not symbols_dict:
            print("Error: Please define symbolic variables first with 'sym' command")
            return

        expr_str = expr_str.replace('^', '**')
        local_dict = {**symbols_dict, 'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'ln': sp.ln, 'exp': sp.exp, 'sqrt': sp.sqrt}
        expr = eval(expr_str, {"__builtins__": None}, local_dict)
        if not isinstance(expr, sp.Basic):
            print("Error: Invalid symbolic expression")
            return
        expressions_dict[expr_name] = (expr, expr_str)
        print(f"Successfully defined expression {expr_name}: {expr_str} = {expr}")
    except NameError as ne:
        print(f"Error: Undefined variable - {ne}")
    except Exception as e:
        print(f"Failed to define expression: {e}")

def handle_show():
    print("\n=== Defined Symbolic Variables ===")
    if symbols_dict:
        for k, v in symbols_dict.items():
            print(f"  {k}: {v}")
    else:
        print("  No symbolic variables")

    print("\n=== Defined Symbolic Expressions ===")
    if expressions_dict:
        for k, (v, s) in expressions_dict.items():
            print(f"  {k}: {s} = {v}")
    else:
        print("  No symbolic expressions")
    print("=" * 30 + "\n")

def handle_simplify(expr_name):
    if expr_name not in expressions_dict:
        print(f"Error: Expression '{expr_name}' does not exist")
        return
    expr, _ = expressions_dict[expr_name]
    simp_expr = sp.simplify(expr)
    print(f"{expr_name} before simplification: {expr}")
    print(f"{expr_name} after simplification: {simp_expr}")

def handle_expand(expr_name):
    if expr_name not in expressions_dict:
        print(f"Error: Expression '{expr_name}' does not exist")
        return
    expr, _ = expressions_dict[expr_name]
    exp_expr = sp.expand(expr)
    print(f"{expr_name} before expansion: {expr}")
    print(f"{expr_name} after expansion: {exp_expr}")

def handle_factor(expr_name):
    if expr_name not in expressions_dict:
        print(f"Error: Expression '{expr_name}' does not exist")
        return
    expr, _ = expressions_dict[expr_name]
    try:
        fac_expr = sp.factor(expr)
        print(f"{expr_name} before factorization: {expr}")
        print(f"{expr_name} after factorization: {fac_expr}")
    except Exception as e:
        print(f"Failed to factorize: {e}")

def handle_diff(cmd):
    parts = cmd.strip().split()
    if len(parts) < 3:
        print("Error: Invalid format, e.g.: diff f1 x 2")
        return
    expr_name, var_name = parts[1], parts[2]
    order = int(parts[3]) if len(parts) >=4 else 1
    if expr_name not in expressions_dict:
        print(f"Error: Expression '{expr_name}' does not exist")
        return
    if var_name not in symbols_dict:
        print(f"Error: Variable '{var_name}' does not exist")
        return
    expr, _ = expressions_dict[expr_name]
    var = symbols_dict[var_name]
    diff_expr = sp.diff(expr, var, order)
    print(f"{order}th order derivative of {expr_name} with respect to {var_name}: {diff_expr}")

def handle_int(cmd):
    parts = cmd.strip().split()
    if len(parts) < 3:
        print("Error: Invalid format, e.g.: int f1 x 0 1")
        return
    expr_name, var_name = parts[1], parts[2]
    if expr_name not in expressions_dict:
        print(f"Error: Expression '{expr_name}' does not exist")
        return
    if var_name not in symbols_dict:
        print(f"Error: Variable '{var_name}' does not exist")
        return
    expr, _ = expressions_dict[expr_name]
    var = symbols_dict[var_name]
    try:
        if len(parts) == 3:
            int_expr = sp.integrate(expr, var)
            print(f"Indefinite integral of {expr_name} with respect to {var_name}: {int_expr} + C")
        else:
            lower = parts[3]
            upper = parts[4]
            if lower == 'oo':
                lower = sp.oo
            elif lower == '-oo':
                lower = -sp.oo
            else:
                lower = eval(lower)
            if upper == 'oo':
                upper = sp.oo
            elif upper == '-oo':
                upper = -sp.oo
            else:
                upper = eval(upper)
            int_expr = sp.integrate(expr, (var, lower, upper))
            print(f"Definite integral of {expr_name} with respect to {var_name} on [{lower}, {upper}]: {int_expr}")
    except Exception as e:
        print(f"Failed to integrate: {e}")

def handle_limit(cmd):
    parts = cmd.strip().split()
    if len(parts) < 4:
        print("Error: Invalid format, e.g.: limit f1 x 0 -")
        return
    expr_name, var_name, point_str = parts[1], parts[2], parts[3]
    direction = parts[4] if len(parts)>=5 else '+'
    if expr_name not in expressions_dict:
        print(f"Error: Expression '{expr_name}' does not exist")
        return
    if var_name not in symbols_dict:
        print(f"Error: Variable '{var_name}' does not exist")
        return
    expr, _ = expressions_dict[expr_name]
    var = symbols_dict[var_name]
    try:
        if point_str == 'oo':
            point = sp.oo
        elif point_str == '-oo':
            point = -sp.oo
        else:
            point = float(point_str)
        lim_expr = sp.limit(expr, var, point, dir=direction)
        print(f"When {var_name} approaches {point} along {direction} direction, the limit of {expr_name} is: {lim_expr}")
    except Exception as e:
        print(f"Failed to calculate limit: {e}")

def handle_solve(cmd):
    parts = cmd.strip().split()
    if len(parts) < 3:
        print("Error: Invalid format, e.g.: solve x**2-4=0 x")
        return
    var_name = parts[-1]
    eq_input = ' '.join(parts[1:-1])

    if var_name not in symbols_dict:
        print(f"Error: Variable '{var_name}' does not exist")
        return
    var = symbols_dict[var_name]
    local_context = {
        var_name: var,
        'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
        'ln': sp.ln, 'log': sp.log, 'exp': sp.exp, 'sqrt': sp.sqrt,
        'pi': sp.pi, 'e': sp.E, 'oo': sp.oo
    }

    try:
        eq_input = eq_input.replace('^', '**')

        if '=' in eq_input:
            lhs_str, rhs_str = eq_input.split('=', 1)
            lhs = parse_expr(lhs_str.strip(), local_dict=local_context)
            rhs = parse_expr(rhs_str.strip(), local_dict=local_context)
            equation = sp.Eq(lhs, rhs)  
        else:
            expr = parse_expr(eq_input.strip(), local_dict=local_context)
            equation = sp.Eq(expr, 0)

        solutions = sp.solve(equation, var)
        if not solutions:
            print(f"No analytical solution for equation {eq_input}")
        else:
            print(f"Solutions for equation {eq_input}:")
            for i, sol in enumerate(solutions, 1):
                print(f"  Solution {i}: {var_name} = {sol}")
    except Exception as e:
        print(f"Failed to solve equation: {e}")

def handle_latex(expr_name):
    if expr_name not in expressions_dict:
        print(f"Error: Expression '{expr_name}' does not exist")
        return
    expr, _ = expressions_dict[expr_name]
    latex_str = sp.latex(expr)
    print(f"LaTeX format of {expr_name}: {latex_str}")

def handle_clear():
    symbols_dict.clear()
    expressions_dict.clear()
    for var in list(globals().keys()):
        if var in symbols_dict:
            del globals()[var]
    print("All symbolic variables and expressions have been cleared")

def main():
    print("===== Welcome to Mini Matlab Symbolic Calculation System =====")
    print("Tip: Enter 'help' to view commands, enter 'exit' to quit the program")
    print("=" * 50 + "\n")
    while True:
        try:
            cmd = input(">>> ").strip()
            if not cmd:
                continue
            cmd_lower = cmd.lower()
            parts = cmd_lower.split()
            main_cmd = parts[0] if parts else ''

            if main_cmd == 'sym':
                handle_sym(cmd)
            elif main_cmd == 'f':
                handle_f(cmd)
            elif main_cmd == 'show':
                handle_show()
            elif main_cmd == 'simplify':
                if len(parts) <2:
                    print("Error: Please specify expression name, e.g.: simplify f1")
                else:
                    handle_simplify(parts[1])
            elif main_cmd == 'expand':
                if len(parts) <2:
                    print("Error: Please specify expression name, e.g.: expand f1")
                else:
                    handle_expand(parts[1])
            elif main_cmd == 'factor':
                if len(parts) <2:
                    print("Error: Please specify expression name, e.g.: factor f1")
                else:
                    handle_factor(parts[1])
            elif main_cmd == 'diff':
                handle_diff(cmd)
            elif main_cmd == 'int':
                handle_int(cmd)
            elif main_cmd == 'limit':
                handle_limit(cmd)
            elif main_cmd == 'solve':
                handle_solve(cmd)
            elif main_cmd == 'latex':
                if len(parts) <2:
                    print("Error: Please specify expression name, e.g.: latex f1")
                else:
                    handle_latex(parts[1])
            elif main_cmd == 'clear':
                handle_clear()
            elif main_cmd == 'help':
                print_help_info()
            elif main_cmd in ['exit', 'quit']:
                print("===== Exiting Program =====")
                break
            else:
                print(f"Error: Unknown command '{main_cmd}', enter 'help' to view available commands")
        except KeyboardInterrupt:
            print("\n===== Exiting Program =====")
            break
        except Exception as e:
            print(f"Execution error: {e}")

if __name__ == "__main__":
    main()