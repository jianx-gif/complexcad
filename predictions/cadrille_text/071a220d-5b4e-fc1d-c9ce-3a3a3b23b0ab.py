import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-51))
w1=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().segment((26,-58),(26,-57)).segment((28,-57)).arc((24,-55),(26,-58)).assemble().finalize().extrude(102).union(w1.sketch().push([(0,1)]).circle(3).circle(2,mode='s').finalize().extrude(-42))