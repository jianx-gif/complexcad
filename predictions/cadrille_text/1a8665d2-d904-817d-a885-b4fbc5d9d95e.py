import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,50))
w1=cq.Workplane('XY',origin=(-100,0,-50))
r=w0.sketch().segment((24,-58),(24,-57)).segment((26,-57)).arc((29,-54),(32,-57)).segment((34,-57)).arc((29,-48),(24,-58)).assemble().finalize().extrude(-100).union(w1.sketch().push([(100,0)]).circle(100).circle(6,mode='s').finalize().extrude(100))