# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 09:35:16 2015

@author: Edward
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt



class spline(object):
    
    def __init__(self,control,knots=None):
        if not isinstance(control,np.ndarray):
            raise TypeError('Control points must be a numpy array')
        if control.dtype != 'float64':
            raise TypeError('Control point array must concist of floats')
        if len(control) != 2:
            raise ValueError('Control point array must have dimension 2.')
        if len(control[0]) <= 3:
            raise ValueError('At least 4 control points are needed')
        self.control = control
        if knots != None:
            if not isinstance(knots,np.ndarray):
                raise TypeError('knots must be a numpy array')
            if knots.dtype != 'float64':
                raise TypeError('knot array must concist of floats.')
            knots.sort()
            if knots[0] != knots[1]:
                knots = np.hstack(([knots[0],knots]))
            if knots[1] != knots[2]:
                knots = np.hstack(([knots[0],knots]))
            if knots[-1] != knots[-2]:
                knots = np.hstack(([knots,knots[-1]]))
            if knots[-2] != knots[-3]:
                knots = np.hstack(([knots,knots[-1]]))
            if len(knots) != len(control[0]) +2:
                raise ValueError('Knot array is of wrong size')
            self.knots = knots
            print(knots)
        else:
            knots = np.linspace(0.,1.,len(control[0])-2)
            self.knots = np.hstack(([0,0],knots,[1,1]))
            print(self.knots)
        
    def __call__(self,u):
<<<<<<< HEAD
        self.u = u        
=======
        if not isinstance(u,np.ndarray):
            raise TypeError('u must be a numpy array')
        if u.dtype != 'float64':
            raise TypeError('u array must concist of floats.')
        u.sort()
        if u[np.argmax(u)] >= self.knots[-1] or u[np.argmin(u)] < self.knots[0]:
            raise ValueError('u out of bounds')
>>>>>>> origin/master
        self.s = self.computeS(u)
        

    @classmethod
    def interpolate(cls, x, y):
        if len(x) != len(y):
            raise NameError('X and Y array of different lengths')
        knots = np.linspace(0.,1.,len(x)-2)
        knots = np.hstack(([0,0],knots,[1,1]))
        cls.knots = knots
        return cls(cls.findD(cls, x, y, knots))
        
        

    def computeS(self,u):
        sX = np.zeros(len(u))
        sY = np.zeros(len(u))
        for i in range(0,len(u)):
            index = self.findHot(u[i])-1
            sX[i] = self.sU(u[i],index,index+1,0)
            sY[i] = self.sU(u[i],index,index+1,1)
        return np.array([sX,sY])
        
    def sU(self,u,rightMost,leftMost,dim):
        #Calculates the blossoms with recursive algorithm
        if rightMost - leftMost == 2:
            return self.control[dim,leftMost]
        elif self.knots[rightMost+1]-self.knots[leftMost-1] == 0:
            alpha = 0#self.knots[rightMost]-u
            return alpha*self.sU(u,rightMost,leftMost-1,dim)+(1-alpha)*self.sU(u,rightMost+1,leftMost,dim)
        else:
            alpha = (self.knots[rightMost+1]-u)/(self.knots[rightMost+1]-self.knots[leftMost-1])
            return alpha*self.sU(u,rightMost,leftMost-1,dim)+(1-alpha)*self.sU(u,rightMost+1,leftMost,dim)
    def findHot(self,u):
        #jomp
        #Finds the interval in which u is.
        return (self.knots > u).argmax()
        
    def findD(self, x, y, knots):
        k=3
        u = knots
        xi = (u[:-2]+u[1:-1]+u[2:])/3.
        
        NMatrix = np.zeros((len(xi),len(xi)))
        for i in range(len(xi)):
            for j in range(len(xi)):
                NMatrix[i,j]=self.makeBasisFunction(self, j,k)(xi[i])
                #NMatrix[[i],[j]]=self.computeNXi(u,k,i,xi[j])
        print(NMatrix)
        dx = sp.linalg.solve(NMatrix,x)
        dy = sp.linalg.solve(NMatrix,y)
        return np.vstack([dx,dy])
        
    def computeNXi(self, u, k, i, xi):
        if k==0:
            if u[i-1] == u[i]:
                return 0
            elif u[i]>xi>=u[i-1]:
                return 1
            else:
                return 0
        else:
            if u[i-1]==u[i+k-1]:
                coef1=0
            else:
                coef1=(xi-u[i-1])/(u[i+k-1]-u[i-1])
            if u[i+k]==u[i]:
                coef2=0
            else:
                coef2=(u[i+k]-xi)/(u[i+k]-u[i])
        NXi = coef1*self.computeNXi(u, k-1, i, xi)+coef2*self.computeNXi(u, k-1, i+1, xi)
        return NXi
    
    def makeBasisFunction(self, j, k):
        def basisFunction(u):
            
            print(j)
            print(k)
            if k==0:
                if self.knots[j-1]==self.knots[j]:
                    return 0
                elif self.knots[j-1]<=u<self.knots[j]:
                    return 1
                else:
                    return 0
            else:
                if self.knots[j+k-1]==self.knots[j-1]:
                    koeff1=0
                else:
                    koeff1=(u-self.knots[j-1])/(self.knots[j+k-1]-self.knots[j-1])
                if self.knots[j+k]==self.knots[j]:
                    koeff2=0
                else:
                    koeff2=(self.knots[j+k]-u)/(self.knots[j+k]-self.knots[j])
                return koeff1*self.makeBasisFunction(self, j,k-1)(u)+koeff2*self.makeBasisFunction(self, j+1,k-1)(u)
        return basisFunction
    def plot(self,plotControl = False):
        
        x = self.s[0]
        y = self.s[1]
        plt.figure(2)
        plt.plot(x,y,'b')
        if plotControl:
            plt.plot(self.control[0],self.control[1],'ro')
            plt.plot(self.control[0],self.control[1],'r--')
        plt.show()
        

    
<<<<<<< HEAD
#def main():
#    plt.close('all')
#control = np.load('controlPoints.npy')
#    knots = np.linspace(0.,1.,len(control[0])-2)
#    knots = np.hstack(([0],knots))
#    u = np.linspace(0.,0.999,1000)
#    Sp = spline(control,knots)
#    Sp(u)
#    Sp.plot()
#main()

u = np.linspace(0.,0.999,1000)
Sp = spline.interpolate(control[0],control[1])
Sp(u)
Sp.plot()


=======
def main():
    plt.close('all')
    control = np.load('controlPoints.npy')
    knots = np.linspace(0.,1.,len(control[0])-2)
    knots = np.hstack(([0, 1],knots))
    u = np.linspace(0.,0.999,1000)
    Sp = spline(control)
    Sp(u)
    Sp.plot(1)
main()
>>>>>>> origin/master

#knots = np.linspace(0,1,12)
#u = np.linspace(0,1,100)
#knots = np.hstack(([0,0],knots,[1, 1]))
#control = np.array([[5.,1,2,3,2,1,-1,2,-3,-4,-5,-5,-7],[4.,-3,2,1,-2,-3,-2,-1,2,3,4,3,6]])
#Sp = spline(knots,control)
#Sp(u)
#Sp.plot()
        
