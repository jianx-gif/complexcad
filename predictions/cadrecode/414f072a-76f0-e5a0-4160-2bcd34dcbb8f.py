import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(100).circle(50,mode='s').push([(-35,-60)]).circle(6,mode='s').push([(80,-11)]).circle(13,mode='s').push([(80,11)]).rect(26,18,mode='s').finalize().extrude(-200)