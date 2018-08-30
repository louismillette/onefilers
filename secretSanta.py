import itertools
import math
import sqlite3
import os

# gets derangements of list of length n
def derangement(n):
    x = range(n)
    p = list(itertools.permutations(list(range(n))))
    return list(i for i in p if not any(i[k] == x[k] for k in range(n)))

# bool replacement_algorithum(list x, int index) produces a true if for all elements of x before index are not index
def replacement_algorithum(x,index):
    i = 0
    while i < index:
        if x[i] == index:
            return False
        i+=1
    return True


# secret_santa_sim(n,lst) takes the number of participents n, the index of the people who got
# themselvs rep, and the list of indexs of know people ( ie, n = 7, rep = [0,3,4], know = [(0,5),(2,6),(3,1)])
# returns the distrabution for each person
def secret_santa_sim(n,rep = [],known = []):
    der = derangement(n)
    for ele in rep:
        der = list(filter(lambda x: replacement_algorithum(x,ele),der))
    for ele in known:
        der = list(filter(lambda x: x[ele[0]] == ele[1],der))
    return der

print(len(secret_santa_sim(7)))
print(len(secret_santa_sim(7)))

# None plot(list<list> possible_derangements, int index) takes all the possible derangements and plots the distrabution
# of possibilities of other index's for the given index

def prob_distrabution(possible_derangements, index):
    y = [ele[index] for ele in possible_derangements]#[3, 10, 7, 5, 3, 4.5, 6, 8.1]
    Y = []
    for ele in range(max(y)+1):
        Y.append((ele,y.count(ele)))
    N = 0
    for ele in Y:
        N += ele[1]
    Y_prime = []
    for ele in Y:
        Y_prime.append((ele[0],float(ele[1]/N)))
    x = print(Y_prime)
    return Y_prime



# prob_distrabution(secret_santa_sim(7, known=[(5,3),(6,1)]),0)

# print(derangement(5))
# print(secret_santa_sim(5, known=[(4,3),(3,1)]))
# prob_distrabution(secret_santa_sim(5, known=[(4,3),(3,1)]),0)


def number_of_derangements(n):
    return math.floor(math.factorial(n)/math.e + 1/2)

# nm derangements are those which use n positional arguments and m free arguments
# where poss. args are numbers which also have a location in the set, and free ones are those
# that dont.  For instance, (1,2,5) has 2 poss. args (1 and 2 are locations in the set, the first and second locations spacifically)
# while 5 is free (there are only 3 locations 1,2,and 3.  5 is free)
def number_of_nm_derangements(n,m):
    if m==0:
        return number_of_derangements(n)
    elif n==0:
        return math.factorial(m)
    else:
        return m * number_of_nm_derangements(n,m-1) + n * number_of_nm_derangements(n-1,m)

# lets find the derangements, except load them from the DB if possible
def number_of_nm_derangements_cached(n,m):
    dirr = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect("{}/derangements.db".format(dirr))
    c = conn.cursor()
    if m==0:
        return number_of_derangements(n)
    elif n==0:
        return math.factorial(m)
    else:
        try:
            mDer = c.execute('SELECT derangement FROM derangements WHERE n={} AND m={}'.format(n,m-1)).fetchone()[0]
        except:
            mDer = None
        try:
            nDer = c.execute('SELECT derangement FROM derangements WHERE n={} AND m={}'.format(n-1, m)).fetchone()[0]
        except:
            nDer = None
        return m * (mDer if mDer else number_of_nm_derangements(n,m-1)) + n * (nDer if nDer else number_of_nm_derangements(n-1,m))

def make_first_n(n):
    dirr = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect("{}/derangements.db".format(dirr))
    c = conn.cursor()
    try:
        c.execute(('CREATE TABLE derangements'
                   '(n INT, '
                   'm INT, '
                   'derangement INT);'))
        conn.commit()
    except:
        pass
    for i in range(n):
        for j in range(i):
            nm = number_of_nm_derangements_cached(j,i-j)
            c.execute('INSERT INTO derangements VALUES("{}", "{}", "{}")'.format(j,i-j,nm))
            conn.commit()
        print("Round {} finished".format(i))


# print(number_of_nm_derangements(25,25))
# print(number_of_derangements(1))
prob_distrabution(secret_santa_sim(4, known=[(3,2)]),0)