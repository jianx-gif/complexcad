import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('ZX',origin=(0,68,0))
r=w0.sketch().segment((-53,27),(-41,27)).arc((-47,30),(-53,27)).assemble().finalize().extrude(-43).union(w0.sketch().push([(0,47.5)]).rect(168,105).push([(0,48)]).circle(21,mode='s').finalize().extrude(11)).union(w1.sketch().segment((-20,-53),(12,-53)).segment((12,53)).segment((-20,53)).segment((-20,20)).arc((-16,23),(-12,25)).segment((-12,44)).segment((8,44)).segment((8,-44)).segment((-12,-44)).segment((-12,-38)).arc((-16,-36),(-20,-33)).close().assemble().finalize().extrude(-168))