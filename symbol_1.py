import math
from collections import defaultdict

class Symbol:
    def __init__(self, name, real=False, positive=False):
        self.name=name
        self.real=real
        self.positive=positive

    def __repr__(self):
        return self.name

    def __str__(self):  
        return self.name

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.name==other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def __add__(self, other):
        if isinstance(other, (int, float, Symbol)):
            return ('+', self, other)
        return NotImplemented

    def __radd__(self, other): 
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, (int, float, Symbol)):
            return ('-', self, other)
        return NotImplemented

    def __rsub__(self, other): 
        return ('-', other, self)

    def __mul__(self, other):
        if isinstance(other, (int, float, Symbol)):
            return ('*', self, other)
        return NotImplemented

    def __rmul__(self, other):  
        return self.__mul__(other)

    def __pow__(self, other):
        if isinstance(other, (int, float)):
            return ('^', self, other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float, Symbol)):
            return ('/', self, other)
        return NotImplemented

    def __rtruediv__(self, other): 
        return ('/', other, self)

def Sin(x):
    return ('sin', x)
def Cos(x): 
    return ('cos', x)
def Log(x): 
    return ('log', x)     
def Exp(x): 
    return ('exp', x)

def expr_to_str(expr):
    if isinstance(expr, (int, float)):
        return str(int(expr) if isinstance(expr, float) and expr.is_integer() else expr)
    if isinstance(expr, Symbol):
        return str(expr)
    if not isinstance(expr, tuple):
        return str(expr)
    
    op = expr[0]
    if op in ('sin', 'cos', 'log', 'exp'):
        arg=expr_to_str(expr[1])
        if isinstance(expr[1], tuple) and expr[1][0] in ('+', '-'):
            arg=f"({arg})"
        return f"{op}({arg})" if op != 'log' else f"ln({arg})"
    
    a, b = expr[1], expr[2]
    def paren(x):
        s = expr_to_str(x)
        if isinstance(x, tuple) and x[0] in ('+', '-'):
            return f"({s})"
        return s

    if op == '+':
        return f"{paren(a)} + {paren(b)}"
    elif op=='-': 
        return f"{paren(a)} - {paren(b)}"
    elif op=='*': 
        return f"{paren(a)}*{paren(b)}"
    elif op=='/': 
        return f"{paren(a)}/{paren(b)}"
    elif op=='^':
        base_str=paren(a) if isinstance(a, tuple) and a[0] in ('+', '-', '*', '/') else expr_to_str(a)
        exp_str=expr_to_str(b)
        return f"{base_str}^{exp_str}"
    else:
        return str(expr)


def parse_term_to_dict(term):
    coeff=1.0
    var_deg=defaultdict(int)

    def _recurse(t):
        nonlocal coeff
        if isinstance(t, (int, float)):
            coeff*=t
        elif isinstance(t, Symbol):
            var_deg[t]+=1
        elif isinstance(t, tuple):
            op = t[0]
            if op=='*':
                _recurse(t[1])
                _recurse(t[2])
            elif op=='^':
                base, exp=t[1], t[2]
                if isinstance(base, Symbol) and isinstance(exp, (int, float)):
                    var_deg[base]+=exp
                else:
                    raise ValueError("Only supports numerical exponents for variables")
            else:
                raise ValueError(f"No {op} allowed in terms")
    _recurse(term)
    return (coeff, dict(var_deg))


def dict_to_term(coeff, var_deg):
    if abs(coeff)<1e-10:
        return 0
    if not var_deg:
        return int(coeff) if isinstance(coeff, float) and coeff.is_integer() else coeff

    parts = []
    for var in sorted(var_deg.keys(), key=lambda v: v.name):
        deg=var_deg[var]
        if deg==1:
            parts.append(var)
        else:
            parts.append(('^', var, deg))
    
    term=parts[0]
    for p in parts[1:]:
        term=('*', term, p)
    
    if coeff!=1:
        term=('*', coeff, term)
    return term


def combine_like_terms(poly):
    if poly==0:
        return 0
    if not isinstance(poly, tuple) or poly[0]!='+':
        return poly

    term_dict=defaultdict(float)

    def _collect(p):
        if not isinstance(p, tuple) or p[0] != '+':
            try:
                coeff, var_deg = parse_term_to_dict(p)
                key=tuple(sorted(var_deg.items(), key=lambda x: x[0].name))
                term_dict[key]+=coeff
            except:
                term_dict[('raw', p)]+=1
        else:
            _collect(p[1])
            _collect(p[2])

    _collect(poly)

    terms=[]
    for key, coeff in term_dict.items():
        if abs(coeff)<1e-10:
            continue
        if key[0]=='raw':
            terms.append(key[1])
        else:
            terms.append(dict_to_term(coeff, dict(key)))

    if not terms:
        return 0
    if len(terms)==1:
        return terms[0]
    
    result = ('+', terms[0], terms[1])
    for t in terms[2:]:
        result=('+', result, t)
    return result

def expand(expr):
    if not isinstance(expr, tuple):
        return expr

    op = expr[0]
    if op=='-':
        return ('+', expand(expr[1]), expand(('*', -1, expr[2])))
    elif op=='+':
        return ('+', expand(expr[1]), expand(expr[2]))
    elif op=='*':
        left=expand(expr[1])
        right=expand(expr[2])
        if isinstance(left, tuple) and left[0]=='+':
            return expand(('+', ('*', left[1], right), ('*', left[2], right)))
        if isinstance(right, tuple) and right[0]=='+':
            return expand(('+', ('*', left, right[1]), ('*', left, right[2])))
        return ('*', left, right)
    else:
        if len(expr)==3:
            return (op, expand(expr[1]), expand(expr[2]))
        return expr

def diff(expr, var):
    if isinstance(expr, Symbol):
        return 1 if expr==var else 0
    if isinstance(expr, (int, float)):
        return 0
    if not isinstance(expr, tuple):
        return 0

    op=expr[0]
    if op=='+':
        return ('+', diff(expr[1], var), diff(expr[2], var))
    elif op=='-':
        return ('-', diff(expr[1], var), diff(expr[2], var))
    elif op=='*':
        u, v=expr[1], expr[2]
        return ('+', ('*', diff(u, var), v), ('*', u, diff(v, var)))
    elif op=='^':
        base,exp=expr[1],expr[2]
        if isinstance(exp,(int, float)):
            return ('*',exp,('^',base,exp-1),diff(base,var))
    elif op=='sin':
        return ('*',Cos(expr[1]),diff(expr[1],var))
    elif op=='cos':
        return ('*',-1,'*',Sin(expr[1]),diff(expr[1],var))
    elif op=='log':
        return ('/',diff(expr[1],var),expr[1])
    elif op=='exp':
        return ('*',Exp(expr[1]),diff(expr[1],var))
    return 0



def integrate(expr,var):
    if isinstance(expr,(int,float)):
        return('*',expr,var)
    if isinstance(expr,Symbol):
        if expr==var:
            return('^',var,2) if var==var else ('/',('^',var,2),2) 
        else:
            return('*', expr,var)  
    
    if not isinstance(expr,tuple):
        return ('*', expr,var)

    op=expr[0]
    if op=='+':
        return ('+', integrate(expr[1], var), integrate(expr[2], var))
    elif op=='-':
        return ('-', integrate(expr[1], var), integrate(expr[2], var))
    elif op=='*':
        left, right=expr[1], expr[2]
        if isinstance(left, (int, float)) or (isinstance(left, Symbol) and left != var):
            return ('*', left, integrate(right, var))
        if isinstance(right, (int, float)) or (isinstance(right, Symbol) and right != var):
            return ('*', right, integrate(left, var))
        return ('int', expr, var)  
    elif op=='^':
        base,exp=expr[1], expr[2]
        if base==var and isinstance(exp, (int, float)) and exp != -1:
            new_exp=exp+1
            return ('/', ('^', var, new_exp), new_exp)
        return ('int', expr, var)
    elif op=='sin':
        arg=expr[1]
        if arg==var:
            return ('*', -1, Cos(var))
        else:
            return ('int', expr, var)  
    elif op=='cos':
        arg=expr[1]
        if arg==var:
            return Sin(var)
        else:
            return ('int', expr, var)
    elif op=='log':
        arg=expr[1]
        if arg==var:
            return ('-', ('*', var, Log(var)), var)  
        else:
            return ('int', expr, var)
    elif op=='exp':
        arg=expr[1]
        if arg==var:
            return Exp(var)
        else:
            return ('int', expr, var)
    else:
        return ('int', expr, var)
