import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.workplane(offset=-193/2).moveTo(24,18).cylinder(193,55).union(w0.sketch().push([(-68,81)]).circle(17).push([(-68,80.5)]).rect(18,19,mode='s').finalize().extrude(-89)).union(w1.sketch().arc((-100,-75),(-91,-74),(-82,-73)).segment((100,-73)).segment((100,73)).segment((-100,73)).close().assemble().push([(0,1)]).circle(71,mode='s').finalize().extrude(-108))