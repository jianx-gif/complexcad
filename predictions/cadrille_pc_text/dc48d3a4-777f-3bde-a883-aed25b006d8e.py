import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,43))
w1=cq.Workplane('XY',origin=(0,0,74))
r=w0.sketch().segment((-6,-1),(6,-1)).segment((6,5)).segment((-6,5)).arc((5,-5),(-6,-1)).assemble().finalize().extrude(-143).union(w0.sketch().circle(69).circle(57,mode='s').finalize().extrude(31)).union(w0.sketch().circle(28).circle(6,mode='s').finalize().extrude(57)).union(w1.sketch().circle(57).push([(-47,0)]).circle(4,mode='s').push([(0,0)]).circle(45,mode='s').finalize().extrude(-108))