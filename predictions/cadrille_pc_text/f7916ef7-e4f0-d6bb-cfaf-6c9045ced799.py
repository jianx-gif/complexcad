import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().rect(200,200).circle(40,mode='s').push([(62,26)]).circle(10,mode='s').finalize().extrude(-40)