import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,24,0))
w1=cq.Workplane('XY',origin=(0,0,-22))
r=w0.sketch().segment((-25,-100),(75,-100)).segment((75,-50)).segment((-25,-50)).segment((-25,-53)).arc((-22,-55),(-25,-57)).close().assemble().push([(24.5,75)]).rect(99,50).finalize().extrude(-50).union(w0.workplane(offset=2/2).moveTo(-25,0).box(100,200,2)).union(w1.sketch().push([(0,-1.5)]).rect(50,47).push([(0,-1)]).circle(23,mode='s').finalize().extrude(95))