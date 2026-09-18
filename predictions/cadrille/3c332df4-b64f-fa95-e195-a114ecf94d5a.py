import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,24,0))
w1=cq.Workplane('XY',origin=(0,0,-25))
r=w0.sketch().push([(25,37)]).rect(100,126).reset().face(w0.sketch().segment((-22,-22),(72,-23)).segment((73,97)).segment((-22,98)).close().assemble(),mode='s').finalize().extrude(-50).union(w0.sketch().push([(-25,0)]).rect(100,200).push([(25,37)]).circle(2,mode='s').finalize().extrude(2)).union(w1.sketch().push([(-75.5,-1.5)]).rect(49,49).push([(-96,-1.5)]).rect(4,29,mode='s').push([(-75,-2)]).circle(20,mode='s').finalize().extrude(100))