import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-83))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-29,-12),(27,-15)).segment((29,14)).segment((-26,14)).close().assemble().finalize().extrude(21).union(w0.sketch().segment((-18,6),(-13,-10)).segment((15,-7)).segment((13,9)).close().assemble().push([(0,1)]).circle(3,mode='s').finalize().extrude(175)).union(w1.workplane(offset=200/2).moveTo(0,-1).box(28,2,200))