import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
r=w0.sketch().circle(20).rect(8,10,mode='s').finalize().extrude(-15).union(w0.sketch().circle(30).circle(29,mode='s').finalize().extrude(10)).union(w0.sketch().circle(27).circle(5,mode='s').push([(15,14)]).circle(3,mode='s').push([(16,-15)]).circle(4,mode='s').finalize().extrude(70))