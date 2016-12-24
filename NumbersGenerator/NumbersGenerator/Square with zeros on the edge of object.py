

from numpy import *

cmatrix = [[1.,1.,0.],[0.,1.,1.]]
imatrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
hmatrix = [[8,3,1],[4,4,1]]


# H COLUMN INIZIALIZATION
convcolumn = []
for i in xrange( len(hmatrix) ):
    for j in xrange( len(hmatrix[i]) ):
        convcolumn.append(hmatrix[i][j])
    for j in xrange( len(cmatrix[0])-1 ):
        convcolumn.append(0.)
for i in xrange( (len(cmatrix) - 1)*(len(hmatrix[0])+len(cmatrix[0])-1) ):
    convcolumn.append(0.)

# END OF H COLUMN INIZIALIZATION

##### GMATRIX INIZIALIZATION
firstrow = []
for j in xrange( len(cmatrix) ):
    for i in xrange( len(cmatrix[j]) ):
        firstrow.append(cmatrix[j][i])
    for i in xrange( len(hmatrix[0])-1 ):
        firstrow.append(0.)
l = len(firstrow)
for j in xrange( len(convcolumn)-l ):
    firstrow.append(0.)

Gmatrix = []
k = 0
for i in xrange( len(hmatrix) ):
    for j in xrange( len(hmatrix[0]) ):
        Gmatrix.append(list(firstrow))
        firstrow.reverse()
        firstrow.pop(0)
        firstrow.append(0.)
        firstrow.reverse()
        k+=1
    for j in xrange( len(cmatrix[0])-1 ):
        firstrow.reverse()
        firstrow.pop(0)
        firstrow.append(0.)
        firstrow.reverse()
        marker = (len(convcolumn)-1)*[0.]
        marker.insert(k, 1.)
        k+=1
        Gmatrix.append(marker)
for i in xrange( (len(cmatrix)-1)*(len(hmatrix[0])+len(cmatrix[0])-1) ):
        marker = (len(convcolumn)-1)*[0.]
        marker.insert(k, 1.)
        k+=1
        Gmatrix.append(marker)

print Gmatrix

    
#END OF GMATRIX INIZIALIZATION


# SOLVING
f = linalg.solve(Gmatrix, convcolumn)
f = array(f).reshape( ( len(hmatrix) + len(cmatrix) - 1, len(hmatrix[0])+len(cmatrix[0])-1 ) )
print f
# END
