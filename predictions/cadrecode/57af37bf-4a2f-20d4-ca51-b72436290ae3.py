import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,56,0))
w1=cq.Workplane('XY',origin=(0,0,-63))
r=w0.sketch().arc((86,-48),(19,-20),(91,-37)).arc((-91,38),(86,-48)).assemble().finalize().extrude(-154).union(w0.sketch().segment((-100,2),(-8,-99)).segment((100,-2)).segment((8,99)).close().assemble().circle(27,mode='s').finalize().extrude(-20)).union(w1.sketch().push([(0,16)]).circle(81).circle(76,mode='s').finalize().extrude(149))