import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-8))
w1=cq.Workplane('XY',origin=(0,0,-10))
r=w0.sketch().circle(43).push([(-30,-10)]).circle(6,mode='s').finalize().extrude(20).union(w1.sketch().segment((-13,-100),(14,-100)).segment((14,-71)).arc((31,-25),(14,21)).segment((14,100)).segment((-13,100)).segment((-13,25)).arc((-93,-25),(-13,-75)).close().assemble().push([(-1,71)]).circle(19,mode='s').push([(73,-42)]).circle(18).finalize().extrude(2))