import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
r=w0.workplane(offset=-10/2).moveTo(1,1).cylinder(10,19).union(w0.sketch().segment((-19,-22),(-13,-26)).segment((-11,-23)).arc((-16,-21),(-19,-18)).close().assemble().reset().face(w0.sketch().arc((-13,13),(-10,15),(-6,16)).segment((-13,20)).close().assemble()).reset().face(w0.sketch().arc((1,-1),(19,-1),(27,-17)).segment((30,-13)).segment((4,8)).close().assemble()).finalize().extrude(-10)).union(w0.sketch().push([(1,1)]).circle(29).circle(21,mode='s').finalize().extrude(8))
