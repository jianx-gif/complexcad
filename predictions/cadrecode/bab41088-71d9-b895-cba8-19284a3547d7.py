import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-26))
w1=cq.Workplane('XY',origin=(0,0,-14))
r=w0.sketch().segment((-61,-29),(-53,-32)).arc((-20,-30),(12,-34)).segment((60,-32)).segment((34,75)).segment((-43,67)).segment((-40,39)).close().assemble().finalize().extrude(-74).union(w0.sketch().segment((-53,-39),(13,-54)).segment((13,-74)).arc((20,31),(-53,-39)).assemble().finalize().extrude(126)).union(w1.sketch().arc((-36,-20),(-34,-21),(-33,-23)).arc((35,33),(-36,-20)).assemble().finalize().extrude(60))