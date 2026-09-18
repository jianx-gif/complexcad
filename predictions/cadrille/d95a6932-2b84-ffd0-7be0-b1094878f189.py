import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-82,-5),(-81,-5)).arc((0,-80),(81,-5)).segment((82,-5)).segment((82,5)).segment((81,5)).arc((0,80),(-81,5)).segment((-82,5)).close().assemble().push([(-2,-1)]).circle(76,mode='s').finalize().extrude(-200)