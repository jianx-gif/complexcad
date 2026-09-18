import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-56))
w1=cq.Workplane('XY',origin=(0,0,-63))
r=w0.sketch().circle(100).push([(45,-22)]).circle(35,mode='s').finalize().extrude(20).union(w0.sketch().circle(80).circle(40,mode='s').finalize().extrude(120)).union(w1.sketch().circle(31).circle(16,mode='s').finalize().extrude(116))