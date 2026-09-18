import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-21,0))
w1=cq.Workplane('ZX',origin=(0,-29,0))
r=w0.sketch().circle(100).circle(66,mode='s').reset().face(w0.sketch().segment((-29,18),(-26,12)).arc((-24,-20),(5,-35)).segment((8,-41)).segment((29,-28)).segment((26,-22)).arc((24,10),(-5,25)).segment((-8,31)).close().assemble()).finalize().extrude(4).union(w1.sketch().arc((-100,-4),(0,-100),(100,-4)).segment((97,-4)).arc((0,-97),(-97,-4)).close().assemble().finalize().extrude(104))