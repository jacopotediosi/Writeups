from z3 import *

# Creating the Solver
s = Solver()

# Creating bitvec
flag = [BitVec("b{0}".format(i), 8) for i in range(42)]
tmp_in = [BitVec("ok{0}".format(i), 32) for i in range(22)]
checksums = [BitVec("ch{0}".format(i), 32) for i in range(22)]

# Original functions translated to python
def zz_helper(x, y, z):
    if y > z:
        return [1, z - x]
    c = zz_helper(y, x + y, z)
    a = c[0]
    b = c[1]
    if b >= x:
        return [2 * a + 1, b - x]
    else:
        return [2 * a, b]
def zz(x):
    return zz_helper(1, 1, x)[0]

# Condition: flag is composed by printable chars
[s.add(flag[i] > 0x20) for i in range(42)]
[s.add(flag[i] < 0x7f) for i in range(42)]

# Dynamic prog (pre-computing all possible zz() values for all range of printable chars)
getV = Function("getV", BitVecSort(8), BitVecSort(8), BitVecSort(32))
for i in range(0x20, 0x7f):
    for j in range(0x20, 0x7f):
        s.add(getV(i, j) == zz(i*256+j))
		
# Original check code translated to python
check_data = [[2, 5, 12, 19, 3749774], [2, 9, 12, 17, 694990], [1, 3, 4, 13, 5764], [5, 7, 11, 12, 299886], [4, 5, 13, 14, 5713094], [0, 6, 8, 14, 430088], [7, 9, 10, 17, 3676754], [0, 11, 16, 17, 7288576], [5, 9, 10, 12, 5569582], [7, 12, 14, 20, 7883270], [
    0, 2, 6, 18, 5277110], [3, 8, 12, 14, 437608], [4, 7, 12, 16, 3184334], [3, 12, 13, 20, 2821934], [3, 5, 14, 16, 5306888], [4, 13, 16, 18, 5634450], [11, 14, 17, 18, 6221894], [1, 4, 9, 18, 5290664], [2, 9, 13, 15, 6404568], [2, 5, 9, 12, 3390622]]

for x in check_data:
    i = x[0]-1
    j = x[1]-1
    k = x[2]-1
    l = x[3]-1
    target = x[4]
    sumz = getV(flag[2*i], flag[2*i+1]) ^ getV(flag[2*j], flag[2*j+1]) ^ getV(flag[2*k], flag[2*k+1]) ^ getV(flag[2*l], flag[2*l+1])
    # Check must be respected
    s.add(sumz == target)
    print(sumz == target)

# Solve the model
print(s.check())
model = s.model()

# Get the flag
definitive_flag=''
for i in range(42):
    print(i, model[flag[i]])
    definitive_flag+=chr(int(str(model[flag[i]])))
print(definitive_flag)