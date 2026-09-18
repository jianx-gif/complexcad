import cadquery as cq
w0=cq.Workplane('YZ',origin=(-21,0,0))
w1=cq.Workplane('ZX',origin=(0,32,0))
r=w0.sketch().push([(0,5)]).circle(23).circle(18,mode='s').finalize().extrude(-39).union(w0.sketch().arc((-27,86),(23,52),(27,-8)).segment((27,75)).segment((-27,75)).close().assemble().finalize().extrude(-12)).union(w0.workplane(offset=47/2).moveTo(0,5).cylinder(47,3)).union(w1.sketch().arc((-100,16),(-5,-59),(100,16)).segment((45,16)).arc((-5,-55),(-55,16)).segment((-71,16)).segment((-71,37)).arc((-64,50),(-65,63)).arc((-79,44),(-100,16)).assemble().finalize().extrude(-63))