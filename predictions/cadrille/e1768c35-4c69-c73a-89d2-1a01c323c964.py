import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-55))
w1=cq.Workplane('ZX',origin=(0,-43,0))
r=w0.sketch().segment((-100,60),(-95,48)).arc((19,42),(63,-43)).segment((75,-39)).segment((49,32)).arc((47,34),(46,37)).segment((39,42)).segment((37,44)).segment((36,43)).segment((2,66)).segment((-54,66)).segment((-54,75)).close().assemble().finalize().extrude(110).union(w1.workplane(offset=-33/2).moveTo(1,75).cylinder(33,25))