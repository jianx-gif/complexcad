import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-4))
w1=cq.Workplane('XY',origin=(0,0,-7))
r=w0.sketch().rect(120,90).push([(-36,-19)]).circle(1,mode='s').push([(39,18)]).circle(2,mode='s').finalize().extrude(7).union(w0.sketch().segment((-29,5),(-24,-18)).segment((29,-5)).segment((24,18)).close().assemble().finalize().extrude(12)).union(w1.sketch().segment((-1,-100),(1,-100)).segment((1,-33)).arc((33,0),(1,33)).segment((1,100)).segment((-1,100)).segment((-1,33)).arc((-33,0),(-1,-33)).close().assemble().finalize().extrude(-1))