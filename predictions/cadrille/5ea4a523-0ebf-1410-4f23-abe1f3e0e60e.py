import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('YZ',origin=(42,0,0))
r=w0.sketch().rect(120,60).reset().face(w0.sketch().segment((-31,-3),(-28,-10)).segment((31,3)).segment((28,10)).close().assemble(),mode='s').push([(50,-5)]).circle(6,mode='s').finalize().extrude(-12).union(w0.sketch().rect(200,60).circle(5,mode='s').finalize().extrude(-12)).union(w1.workplane(offset=58/2).box(20,8,58))