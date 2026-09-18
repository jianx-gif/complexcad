import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-12))
w1=cq.Workplane('XY',origin=(0,0,3))
r=w0.sketch().segment((-100,-62),(100,-62)).segment((100,62)).segment((98,62)).arc((97,60),(95,62)).segment((-100,62)).close().assemble().circle(38,mode='s').finalize().extrude(-20).union(w1.sketch().segment((0,-100),(20,-100)).segment((20,-17)).arc((24,0),(20,17)).segment((20,100)).segment((0,100)).segment((0,24)).arc((-24,0),(0,-24)).close().assemble().circle(6,mode='s').finalize().extrude(-16))