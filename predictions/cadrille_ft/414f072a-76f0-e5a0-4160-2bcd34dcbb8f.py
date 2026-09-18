import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(100).circle(50,mode='s').push([(80.0,0)]).rect(35,40,mode='s').finalize().extrude(-200)