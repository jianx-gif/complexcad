import cadquery as cq
w0=cq.Workplane('XY',origin=(-60,-60,-100))
r=w0.sketch().segment((28,-28),(28,-26)).segment((31,-26)).arc((-30,27),(28,-28)).assemble().circle(30,mode='s').finalize().extrude(200)