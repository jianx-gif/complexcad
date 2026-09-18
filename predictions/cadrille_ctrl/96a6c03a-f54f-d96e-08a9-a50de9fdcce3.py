import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
w1=cq.Workplane('ZX',origin=(0,16,0))
r=w0.sketch().segment((-27,10),(-19,-24)).segment((-12,-22)).arc((-20,-7),(-19,9)).segment((-21,11)).close().assemble().reset().face(w0.sketch().arc((11,28),(22,12),(23,-7)).segment((29,-6)).segment((20,29)).close().assemble()).finalize().extrude(-12).union(w0.sketch().segment((-19,-14),(-18,-24)).segment((27,-19)).segment((26,-9)).close().assemble().finalize().extrude(-12)).union(w0.sketch().segment((-11,13),(12,-1)).segment((14,2)).segment((-8,16)).close().assemble().finalize().extrude(17)).union(w1.sketch().segment((12,-10),(12,-9)).segment((13,-9)).arc((-13,1),(12,-10)).assemble().finalize().extrude(-3))
