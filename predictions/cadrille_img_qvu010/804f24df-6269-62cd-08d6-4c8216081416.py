import cadquery as cq
w0=cq.Workplane('YZ',origin=(95,0,0))
w1=cq.Workplane('ZX',origin=(0,-45,0))
r=w0.sketch().segment((-69,36),(-68,36)).segment((-56,-36)).segment((-56,-45)).segment((40,-29)).segment((33,17)).segment((-56,-1)).segment((-56,36)).segment((-53,36)).segment((-53,45)).close().assemble().finalize().extrude(-195).union(w1.sketch().arc((-94,45),(-88,37),(-81,30)).arc((-33,81),(34,58)).arc((41,60),(48,62)).arc((-30,96),(-94,45)).assemble().finalize().extrude(134))