import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,1,0))
w1=cq.Workplane('ZX',origin=(0,89,0))
r=w0.sketch().arc((-55,-39),(-20,-1),(29,14)).segment((55,39)).segment((55,55)).arc((11,38),(-29,55)).segment((-29,39)).arc((-78,1),(-55,-55)).close().assemble().finalize().extrude(-91).union(w0.sketch().push([(0,1)]).circle(69).push([(35,-27)]).circle(47,mode='s').finalize().extrude(-12)).union(w0.workplane(offset=59/2).moveTo(0,1).cylinder(59,45)).union(w1.sketch().arc((-79,-22),(100,1),(-79,22)).arc((-100,0),(-79,-22)).assemble().push([(23,1)]).circle(77,mode='s').finalize().extrude(-154))