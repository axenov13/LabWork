from numpy import *

cmatrix = [[1,3],[4,1]]
imatrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
hmatrix = [[4,2,8],[3,4,1]]


# H COLUMN INIZIALIZATION
convcolumn = []
for i in range( len(hmatrix) ):
    for j in range( len(hmatrix[i]) ):
        convcolumn.append(hmatrix[i][j])
# END OF H COLUMN INIZIALIZATION


##### GMATRIX INIZIALIZATION
firstrow = []
for j in range( len(cmatrix) ):
    for i in range( len(cmatrix[j]) ):
        firstrow.append(cmatrix[j][i])
    for i in range( len(hmatrix[j])-1 ):
        firstrow.append(0)
while len(firstrow) < ( len(hmatrix[0]) + len(cmatrix[0]) - 1 )*( len(cmatrix) + len(hmatrix) - 1 ):
    firstrow.append(0)

Gmatrix = []
Gmatrix.append(list(firstrow))
while len(Gmatrix) < len(convcolumn):
    firstrow.reverse()
    firstrow.pop(0)
    firstrow.append(0)
    firstrow.reverse()
    Gmatrix.append(list(firstrow))
#END OF GMATRIX INIZIALIZATION

# SOLVING
f = linalg.lstsq(Gmatrix, convcolumn)[0]
f = array(f).reshape( ( len(hmatrix) + len(cmatrix) - 1, len(hmatrix[0])+len(cmatrix[0])-1 ) )
print f
# END
