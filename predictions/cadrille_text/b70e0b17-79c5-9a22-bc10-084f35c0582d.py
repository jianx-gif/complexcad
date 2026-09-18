import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-54))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((29,-58),(35,-58)).segment((35,-55)).arc((32,-56),(29,-58)).assemble().finalize().extrude(154).union(w1.sketch().arc((53,100),(56,98),(58,95)).segment((58,100)).close().assemble().finalize().extrude(47))