import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-26))
w1=cq.Workplane('XY',origin=(0,0,-23))
r=w0.sketch().segment((-100,-45),(-41,-45)).arc((-1,-3),(41,-45)).segment((100,-45)).arc((87,-17),(69,6)).arc((54,36),(21,39)).arc((-44,43),(-82,-10)).arc((-93,-28),(-100,-45)).assemble().push([(-34,15)]).circle(7,mode='s').push([(34,15)]).circle(7,mode='s').finalize().extrude(52).union(w1.sketch().push([(0,20.5)]).rect(90,49).push([(0,20)]).circle(23,mode='s').finalize().extrude(40))