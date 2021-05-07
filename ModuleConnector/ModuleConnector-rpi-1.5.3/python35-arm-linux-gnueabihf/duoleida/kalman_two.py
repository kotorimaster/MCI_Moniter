import numpy as np
class Kalman_two:
    def __init__(self,xx,vv):
        self.B = 0
        self.u = 0
        self.K = 0
        self.z = 0
        self.P = np.zeros((2, 2))
        self.x = np.transpose(np.array([xx, vv]))#(2,1)
        self.x=np.reshape(self.x,[2,1])

        self.A = np.array([[1, 0.2], [0, 1]])
        self.Q = np.array([[0.01, 0], [0, 0.012]])
        self.H = np.array([1, 0])  # (1,2)
        self.H=np.reshape(self.H,[1,2])
        self.R = np.array([3])

    def kf_update(self):
        x_=np.dot(self.A,self.x)+np.dot(self.B,self.u)#(2,1)
        x_=np.reshape(x_,[2,1])

        p_=np.dot(np.dot(self.A,self.P),np.transpose(self.A))+self.Q#(2,2)

        iv=float(np.dot(np.dot(self.H,p_),np.transpose(self.H))+self.R)
        iv2=1/iv

        self.K=np.dot(p_,np.transpose(self.H))*iv2#(2,1)
        self.K=np.reshape(self.K,[2,1])

        self.x=x_+self.K*(self.z-np.dot(self.H,x_))#(2,1)

        self.P=p_-np.dot(np.dot(self.K,self.H),p_)#(2,2)






