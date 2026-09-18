import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-15))
r=w0.sketch().segment((-100,-62),(100,-62)).segment((100,62)).segment((-100,62)).segment((-100,24)).arc((-76,-6),(-100,-36)).close().assemble().push([(-40,-24)]).circle(6,mode='s').finalize().extrude(-20).union(w0.sketch().push([(-37.5,0)]).rect(15,74).push([(37.5,0)]).rect(15,74).finalize().extrude(50))