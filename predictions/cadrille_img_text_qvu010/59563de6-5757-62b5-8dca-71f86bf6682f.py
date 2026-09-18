import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,60,0))
r=w0.sketch().push([(-31,-29)]).circle(47).push([(25,25)]).circle(55).finalize().extrude(-200).union(w1.sketch().arc((-97,-31),(-46,-90),(29,-73)).arc((46,89),(-58,-39)).arc((-82,-48),(-97,-29)).close().assemble().push([(25,25)]).circle(70,mode='s').finalize().extrude(-81))