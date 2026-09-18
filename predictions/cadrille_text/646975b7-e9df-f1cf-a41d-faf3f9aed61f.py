import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((29,-58),(29,-57)).segment((32,-57)).segment((32,-58)).arc((34,-57),(36,-55)).segment((36,-54)).segment((38,-54)).arc((42,-49),(45,-42)).segment((45,-41)).segment((46,-41)).arc((-37,49),(29,-58)).assemble().finalize().extrude(100)