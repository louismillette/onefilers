from sympy.solvers.diophantine import diop_solve
from sympy import *
from sympy import symbols
import np
A,L,D,B,n,t_0 = symbols("A, L, D, B, n, t_0", integers=True)
'''
laundry_basic(bal,L,P) -> list<tuples>
    laundry_basic finds the solution to the equation 10*A + bal = P*L,
    the diophantine equation that gives the pairs (A,L) of solutions to the basic
    laundry problem for parameters bal,P

    bal: amount of money on starting on the card
    A: Money put on card, in units of $10 (A = 2 represents $20)
    L: Full loads
    P: Price per load
'''
def laundry_basic(bal,P):
    eqn = diop_solve(1000 * A + int(bal * 100) - int(100 * P) * L)
    print('L, A')
    for intiger in [-1,-2,-3,-4]:
        a = sympify(str(eqn[0]).replace('t_0',str(intiger)))
        l = sympify(str(eqn[1]).replace('t_0',str(intiger)))
        print(l,a)

laundry_basic(0, 4.2)

'''
The Dry Laundry Equation:
    10*A+1.6 = 4.2*L + 1.85B
    A: number of $10 to put on the card
    L: number of loads
    B: number of just washes
has solution:
    B = 44A + 84C + 44 AND
    L = -17A-37C-19

x is accuracy.  Higher x higher accuracy.
'''

#IB: initial balance
#WD: wash, dry

def diOp(bal,A,n_2):
    eqn = diop_solve(1000*A + int(bal*100) - 185*D -235*B - 420*L)
    expr = sympify((str(eqn[3])).replace("t_1","n"))
    print(expr)
    ineq = list(solve(sympify(expr))[0].items())
    print(ineq)
    print(ineq.replace('t_0','A'))
    # x = eval(str(ineq.replace("t_0","1")))
    # print(floor(x)+2)
    # print(floor(x) - 2)
    print([eqn],ineq)
    sig,num = checkGL(ineq,eqn[-1],A,n_2)
    return eqn,ineq,sig,num

def checkGL(ineq,L,A,n_2):
    x = floor(eval(str(ineq.replace("t_0", str(A)).replace("t_2", str(n_2))))) + 1
    expr = eval(str(L).replace("t_0", str(A)).replace("t_2",str(n_2)).replace("t_1",str(x)))
    if expr > 0:
        return ">",x
    else:
        return "<",x-1

# x for accuracy and bal for balance
def Dry(x,bal):
    A = 1
    while A <= 4:
        n_2 = x
        while n_2 >= 0:
            eqn, ineq, sig, num = diOp(bal,A,n_2)
            print(eqn)
            break #debug
            if(sig==">"):
                n_1 = num
                while n_1 < x + num:
                    A = eqn[1]

                    pass # set vars here
                    n_1 += 1
            else:
                n_1 = num
                while n_1 > -x:
                    pass # set vars here
                    n_1 -= 1

            n_2 -= 1
        break
        while c < (-19/37)-(-17/37)*A:
            break
            L = -17*A-37*c-19
            B = 44*A+84*c+44
            if abs(B) <= 20:
                print(A,L,D,B)
            c += 1
        A += 1


#Dry(5,1.6)


'''
The Wash Laundry Equations:
    10*A+1.6 = 4.2*L + 2.35B
    A: number of $10 to put on the card
    L: number of loads
    B: number of just washes
has solution:
    B = 40A + 84C + 40 AND
    L = -20A-47C-22

x is accuracy.  Higher x higher accuracy.
'''



#Dry(10)