import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-14,0))
w1=cq.Workplane('YZ',origin=(-1,0,0))
r=w0.sketch().segment((-20,13),(-1,-11)).segment((11,-2)).segment((-4,17)).segment((-3,18)).segment((-4,18)).segment((-4,35)).segment((-6,30)).segment((-10,26)).segment((-10,13)).close().assemble().finalize().extrude(29).union(w0.sketch().segment((-19,13),(-13,13)).segment((-13,14)).segment((-19,14)).close().assemble().finalize().extrude(29)).union(w1.sketch().segment((-14,51),(-12,51)).segment((-12,49)).segment((14,49)).segment((14,51)).segment((15,51)).segment((15,56)).segment((14,56)).segment((14,57)).segment((-12,57)).segment((-12,56)).segment((-14,56)).close().assemble().push([(0,54)]).circle(3,mode='s').finalize().extrude(-17))
