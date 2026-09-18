import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-80))
w1=cq.Workplane('YZ',origin=(15,0,0))
r=w0.sketch().circle(99).reset().face(w0.sketch().segment((-60,-58),(-56,-58)).segment((-56,-60)).segment((56,-60)).segment((56,-58)).segment((60,-58)).segment((60,58)).segment((56,58)).segment((56,60)).segment((-56,60)).segment((-56,58)).segment((-60,58)).close().assemble(),mode='s').push([(93,-5)]).circle(4,mode='s').finalize().extrude(160).union(w1.sketch().rect(200,180).rect(120,140,mode='s').finalize().extrude(-30))