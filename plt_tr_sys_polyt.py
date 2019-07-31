import polytope as pc
from polytope import plot
import numpy as np
from read_data import ReadData
import nose
import unittest
import matplotlib.pyplot as plt
import sys
from trans_sys_polytope import TransSysToPolytope as tran_sys

def _get_patch(poly1, **kwargs):
    """Return matplotlib patch for given Polytope.

    Example::

    > # Plot Polytope objects poly1 and poly2 in the same plot
    > import matplotlib.pyplot as plt
    > fig = plt.figure()
    > ax = fig.add_subplot(111)
    > p1 = _get_patch(poly1, color="blue")
    > p2 = _get_patch(poly2, color="yellow")
    > ax.add_patch(p1)
    > ax.add_patch(p2)
    > ax.set_xlim(xl, xu) # Optional: set axis max/min
    > ax.set_ylim(yl, yu)
    > plt.show()

    @type poly1: L{Polytope}
    @param kwargs: any keyword arguments valid for
        matplotlib.patches.Polygon
    """
    import matplotlib as mpl
    V = pc.extreme(poly1)
    rc, xc = pc.cheby_ball(poly1)
    x = V[:, 1] - xc[1]
    y = V[:, 0] - xc[0]
    mult = np.sqrt(x**2 + y**2)
    x = x / mult
    angle = np.arccos(x)
    corr = np.ones(y.size) - 2 * (y < 0)
    angle = angle * corr
    ind = np.argsort(angle)
    # create patch
    patch = mpl.patches.Polygon(V[ind, :], True, **kwargs)
    patch.set_zorder(0)
    return patch

A =np.asarray(ReadData.A[len(ReadData.A) -1])
b =np.asarray(ReadData.B[len(ReadData.B) -1])

# A = np.array([[-1,0],[1,0],[0,-1],[0,1],[-3,-5],[1,-1],[-1,2.5],[-2,2.5]])
# b = np.array([[-5,-7,-3,-6,-15,-7,-15,-17.5]])
class PlotTraSys:
    print("Plotting transition system on polytopes")

    # def testAndbConsistency(self):
    #     self.assertTrue(np.shape(A)[0 == np.shape(b)[0]])

    if(np.shape(A)[0] == np.shape(b)[0]):
        pass
    else:
        print("Ensure the number of row of A and b matrix corresponding to the state space boundaries are same")


    p = pc.Polytope(A,b)
    Bound = pc.extreme(p)
    if(isinstance(Bound,type(None))):
        p = pc.Polytope(A,-1*b)
        Bound = pc.extreme(p)
        print("Tried with reversing the signs of b matrix")

    if(isinstance(Bound,type(None))):
        print("PLease make sure the state space boundaries form a convex polytope")
        sys.exit(1)

    n = np.shape(A)[1] #space dimension

    if(n == 2):
        ep = (np.amax(Bound, axis=0) - np.amin(Bound,axis=0))/20
        # ep = np.reshape(ep,(1,2))
        xmin = np.amin(Bound[:,0]) - ep[0]
        xmax = np.amax(Bound[:,0]) + ep[0]
        ymin = np.amin(Bound[:,1]) - ep[1]
        ymax = np.amax(Bound[:,1]) + ep[1]
         # p.plot()
        # plt.xlim(xmin,xmax)
        # plt.ylim(ymin,ymax)
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # plt.figure(1)
        pad_no = str(len(str(len(tran_sys.Tp_Q))) +1)
        centr = np.zeros((len(tran_sys.Tp_Q),n))
        for i in range(len(tran_sys.Tp_Q)):
            k = pc.qhull(tran_sys.Tp_vert[i])
            tmp = _get_patch(k,color="blue")
            ax.add_patch(tmp)


            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
            # plt.figure(1)
            plt.show()



        plt.show()

    elif( n ==3):
        print()
    else:
        print("Cannot display more than 3 dimension transition system")

    # p.plot()
    # plt.ylim(-8,8)
    # plt.xlim(-8,8)
    # plt.show()
    #
    #
    # print(p)
    # v = pc.extreme(p)
    # V_rep = np.array([[-5,0],[0,-3],[7,0],[4,-3],[7,6],[0,6],[-2.5,5],[-5,3]])
    #
    # tmp = pc.qhull(V_rep)
    # print(tmp)
    print("$#$####")

# if __name__ == '__main__':
#     unittest.main()