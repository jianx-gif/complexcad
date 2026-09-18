import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,45))
r=w0.sketch().arc((-18,-1),(-16,-1),(-16,-4)).arc((16,5),(-18,-1)).assemble().push([(0,0)]).circle(8,mode='s').finalize().extrude(-45).union(w0.sketch().segment((-29,-7),(-27,-14)).segment((-23,-13)).arc((7,-29),(28,-3)).segment((32,-2)).segment((30,5)).segment((26,4)).arc((-4,29),(-26,-4)).close().assemble().push([(1,1)]).circle(8,mode='s').finalize().extrude(-16)).union(w0.workplane(offset=-16/2).moveTo(1,0).cylinder(16,29))
