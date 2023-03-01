
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


