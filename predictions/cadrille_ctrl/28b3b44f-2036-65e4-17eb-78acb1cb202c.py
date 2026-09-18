import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
r=w0.sketch().segment((-2,-20),(-2,-18)).segment((2,-18)).segment((2,-20)).arc((1,20),(-2,-20)).assemble().circle(5,mode='s').finalize().extrude(-15).union(w0.sketch().circle(30).push([(12,1)]).circle(15,mode='s').finalize().extrude(11)).union(w0.sketch().circle(27).circle(5,mode='s').push([(15,-15)]).circle(3,mode='s').finalize().extrude(70))
