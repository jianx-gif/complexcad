import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-29,0))
w1=cq.Workplane('ZX',origin=(0,-10,0))
r=w0.sketch().arc((-100,-40),(0,10),(100,-40)).segment((100,40)).segment((89,40)).segment((89,90)).segment((-89,90)).segment((-89,40)).segment((-100,40)).close().assemble().finalize().extrude(12).union(w1.sketch().arc((-99,-40),(0,1),(99,-40)).segment((99,40)).segment((-99,40)).close().assemble().finalize().extrude(-59))