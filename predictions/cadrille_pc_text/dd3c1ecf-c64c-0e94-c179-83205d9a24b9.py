import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-4))
r=w0.sketch().segment((-80,-51),(0,-51)).segment((0,48)).segment((-15,48)).segment((-15,51)).segment((-80,51)).close().assemble().finalize().extrude(-5).union(w0.sketch().rect(200,150).circle(75,mode='s').finalize().extrude(13))