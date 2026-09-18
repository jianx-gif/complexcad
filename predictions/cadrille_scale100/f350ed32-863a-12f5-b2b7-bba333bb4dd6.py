import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,6))
w1=cq.Workplane('ZX',origin=(0,0,0))
r=w0 topun (50 (10,0))
w1 On (10,0))
w1 On con S.

r=w0.sketch().segment((-30,15),(-29,15)).segment((-29,16)).segment((-30,16)).close().assemble().finalize().extrude(-14).union(w0.sketch().segment((-30,15),(-29,15)).segment((-29,16)).segment((-30,16)).close().assemble().finalize().extrude(-11)).union(w0.sketch().segment((-30,10),(-29,10)).segment((-29,11)).segment((-30,11)).close().assemble().finalize().extrude(16)).union(w0.sketch().segment((15,-1),(27,-15)).segment((30,-12)).segment((16,1)).close().assemble().finalize().extrude(-11)).union(w0.sketch().segment((15,11),(27,11)).segment((22,16)).close().assemble().finalize().extrude(16)).union(w1 (50,99),(-100,6)).segment((-99,6)).segment((-99,5)).segment((-98,5)).segment((-98,6)).segment((-97,6)).segment((-97,7)).segment((-96,6)).segment((-99,6)).segment((-99,5)).segment((-100,5)).segment((-100,4)).close().assemble().finalize().extrude(12))