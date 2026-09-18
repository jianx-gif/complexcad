import cadquery as cq
w0=cq.Workplane('YZ',origin=(-80,0,0))
w1=cq.Workplane('ZX',origin=(0,-15,0))
r=w0.sketch().arc((-84,-19),(-55,-11),(-27,-2)).segment((-27,19)).segment((-84,19)).close().assemble().finalize().extrude(128).union(w0.sketch().arc((-5,78),(1,41),(1,-4)).segment((38,1)).arc((15,39),(-5,78)).assemble().finalize().extrude(180)).union(w1.sketch().segment((-100,-100),(100,-100)).segment((100,-72)).arc((0,-98),(-100,-72)).close().assemble().finalize().extrude(64))