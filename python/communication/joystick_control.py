from math import pi, cos, sin
import numpy as np

articulation_select = {'0':7,'1':'mode_pince','4':2,'5':3,'6':4,'7':5,'8':6}

def pilotage(articulation_old, mode_pince, mode, value, vmax):
   if mode == 'articulation':
      vitesse = [0,0,0,0,0,0,0]
      if value['type'] == 'buttondown':
         button = articulation_select[str(value['valeur']['button'])]
         if button == 'mode_pince':
            mode_pince=-mode_pince
         elif button == 7:
            vitesse[6] = mode_pince*vmax/2
            button = articulation_old
      elif value['type'] == 'buttonup':
         button = articulation_old
         buttonup = articulation_select[str(value['valeur']['button'])]
         if buttonup == 7:
            vitesse[6] = 0
      elif value['type'] == 'joystick':
         button = articulation_old
         rot_base = value['valeur']['Axis 2'] * vmax
         rot_articulation = -value['valeur']['Axis 1'] * vmax
         vitesse[0] = rot_base
         for i in range(1,6):
            if i == button-1:
               vitesse[i] = rot_articulation
            else:
               vitesse[i] = 0
      return button, mode_pince, {'mode':'run','vitesses': vitesse}


   if mode == 'mci':
      vitesse = [0,0,0,0,0,0,0]
      if value['type'] == 'joystick':
         vx = value['valeur']['Axis 0']*vmax
         vy = value['valeur']['Axis 1']*vmax
         vz = value['valeur']['Axis 2']*vmax
         vitesse = calculMCI(vx,vy,vz,0,0,0)

      return articulation_old, mode_pince, {'mode':'run','vitesses': vitesse}

def calculMCI(vx,vy,vz,wx,wy,wz):
   r1 = 0.1235
   d2 = 0.1745
   d3 = 0.145
   d4 = 0.193
   d5 = 0.044
   r5 = 0.250
   r7 = 0.17255
   offsetq1 = 0
   offsetq2 = 0
   offsetq3 = 2*pi/6
   offsetq4 = 0
   offsetq5 = 0
   offsetq6 = 0
   offsetq7 = 0

   qj = [0, 0, 0, 0, 0, -pi, pi/2];
   q1 = offsetq1 + qj[0];
   q2 = offsetq2 + qj[1];
   q3 = offsetq3 + qj[2];
   q4 = offsetq4 + qj[3];
   q5 = offsetq5 + qj[4];
   q6 = offsetq6 + qj[5];

   T01=np.array([[cos(q1), -sin(q1), 0, 0],[sin(q1), cos(q1), 0, 0],[0, 0, 1, r1],[ 0, 0, 0, 1]])
   T12=np.array([[cos(q2), -sin(q2), 0, d2],[0, 0, -1, 0],[sin(q2), cos(q2), 0, 0],[ 0, 0, 0, 1]])
   T23=np.array([[cos(q3), -sin(q3), 0, d3],[sin(q3), cos(q3), 0, 0],[0, 0, 1, 0],[ 0, 0, 0, 1]])
   T34=np.array([[cos(q4), -sin(q4), 0, d4],[sin(q4), cos(q4), 0, 0],[0, 0, 1, 0],[ 0, 0, 0, 1]])
   T45=np.array([[cos(q5), -sin(q5), 0, d5],[0, 0, -1, -r5],[sin(q5), cos(q5), 0, 0],[ 0, 0, 0, 1]])
   T56=np.array([[cos(q6), -sin(q6), 0, 0],[0, 0, -1, 0],[sin(q6), cos(q6), 0, 0],[0, 0, 0, 1]])
   T67=np.array([[1, 0, 0, 0],[ 0, 0, -1, -r7],[0, 1, 0, 0],[ 0, 0, 0, 1]])

   T02 = np.dot(T01,T12)
   T03 = np.dot(T02,T23)
   T04 = np.dot(T03,T34)
   T05 = np.dot(T04,T45)
   T06 = np.dot(T05,T56)
   T07 = np.dot(T06,T67)

   J0 = np.zeros((6,7))

   J0[0:3,0] = np.cross(T01[0:3,2],(T07[0:3,3]-T01[0:3,3]))
   J0[0:3,1] = np.cross(T02[0:3,2],(T07[0:3,3]-T02[0:3,3]))
   J0[0:3,2] = np.cross(T03[0:3,2],(T07[0:3,3]-T03[0:3,3]))
   J0[0:3,3] = np.cross(T04[0:3,2],(T07[0:3,3]-T04[0:3,3]))
   J0[0:3,4] = np.cross(T05[0:3,2],(T07[0:3,3]-T05[0:3,3]))
   J0[0:3,5] = np.cross(T06[0:3,2],(T07[0:3,3]-T06[0:3,3]))
   J0[0:3,6] = np.cross(T07[0:3,2],(T07[0:3,3]-T07[0:3,3]))

   J0[3:6,0]=T01[0:3,2]
   J0[3:6,1]=T02[0:3,2]
   J0[3:6,2]=T03[0:3,2]
   J0[3:6,3]=T04[0:3,2]
   J0[3:6,4]=T05[0:3,2]
   J0[3:6,5]=T06[0:3,2]
   J0[3:6,6]=T07[0:3,2]

   Jpseudoinv=np.dot((J0.T),np.linalg.inv((np.dot(J0,(J0.T)))))
   qp = np.dot(Jpseudoinv,np.array([vx,vy,vz,wx,wy,wz]))
   return qp
