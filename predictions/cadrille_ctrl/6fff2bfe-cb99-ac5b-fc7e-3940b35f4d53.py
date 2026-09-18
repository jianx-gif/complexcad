import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.workplane(offset=-84/2).moveTo(0,-1).cylinder(84,2).union(w0.sketch().push([(0,-1)]).circle(29).circle(20,mode='s').finalize().extrude(80)).union(w0.sketch().push([(0,-1)]).circle(33).circle(30,mode='s').finalize().extrude(83))
