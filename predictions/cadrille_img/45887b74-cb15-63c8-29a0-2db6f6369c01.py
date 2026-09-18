import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-87,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-95,-46),(-77,28),(-95,100)).segment((-95,46)).segment((-93,46)).segment((-95,39)).close().assemble().finalize().extrude(155).union(w1.sketch().arc((-84,-39),(-52,-36),(-22,-26)).arc((-19,18),(10,53)).arc((-32,36),(-70,51)).arc((-76,45),(-84,41)).close().assemble().push([(-46,28)]).circle(5,mode='s').finalize().extrude(-166))