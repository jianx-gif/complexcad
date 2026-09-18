import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
w1=cq.Workplane('YZ',origin=(-8,0,0))
r=w0.sketch().segment((-100,19),(-99,19)).segment((-99,18)).segment((-98,18)).segment((-98,19)).segment((-97,19)).segment((-97,21)).segment((-98,21)).segment((-99,21)).segment((-100,21)).segment((-100,19)).close().assemble().finalize().extrude(-3).union(w0.sketch().segment((-10,1),(-4,0)).segment((-3,5)).segment((-9,6)).close().assemble().finalize().extrude(-4)).union(w0.sketch().segment((97,1),(97,1)).segment((98,1)).segment((98,0)).arc((99,3),(97,1)).assemble().finalize().extrude(11)).union(w0.sketch().push([(0,71)]).circle(8).push([(0,71.5)]).rect(10,3,mode='s').finalize().extrude(16))
