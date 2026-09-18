import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,9))
w1=cq.Workplane('ZX',origin=(0,-5,0))
r=w0.sketch().rect(200,150).rect(158,10,mode='s').finalize().extrude(-13).union(w1.sketch().segment((-9,-58),(9,-58)).segment((9,-22)).arc((0,-23),(-9,-22)).close().assemble().finalize().extrude(69))