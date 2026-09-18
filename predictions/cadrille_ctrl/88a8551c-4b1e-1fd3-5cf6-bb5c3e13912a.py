import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-50,-40),(50,-40)).segment((50,40)).segment((15,40)).segment((15,60)).segment((-15,60)).segment((-15,40)).segment((-50,40)).close().assemble().reset().face(w0.sketch().segment((-45,-35),(45,-35)).segment((45,35)).segment((-45,35)).segment((-45,-12)).arc((-48,-20),(-45,-28)).close().assemble(),mode='s').finalize().extrude(-8).union(w0.sketch().rect(86,70).push([(-31,-16)]).circle(2,mode='s').finalize().extrude(-4)).union(w0.workplane(offset=6/2).box(90,10,6))
