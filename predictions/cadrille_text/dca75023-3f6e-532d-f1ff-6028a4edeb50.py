import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,-56,-100))
r=w0.sketch().segment((-53,15),(-37,15)).segment((-37,11)).segment((37,11)).segment((37,15)).segment((53,15)).segment((53,17)).segment((57,17)).segment((57,15)).segment((59,15)).arc((1,56),(-53,15)).assemble().finalize().extrude(200)