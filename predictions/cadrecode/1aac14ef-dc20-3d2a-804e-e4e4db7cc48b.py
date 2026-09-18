import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((-78,-72),(-74,-72)).segment((-74,-100)).segment((100,-100)).segment((100,-15)).segment((90,-15)).segment((90,-11)).segment((-78,-11)).close().assemble().finalize().extrude(-12).union(w0.sketch().segment((-100,87),(-12,-27)).segment((27,3)).segment((-80,100)).close().assemble().finalize().extrude(12))