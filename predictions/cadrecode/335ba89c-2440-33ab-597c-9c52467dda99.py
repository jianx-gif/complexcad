import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-37))
w1=cq.Workplane('XY',origin=(0,0,-35))
r=w0.sketch().segment((-100,-64),(-97,-64)).segment((-97,-75)).segment((99,-75)).segment((99,-64)).segment((100,-64)).segment((100,-41)).segment((99,-41)).segment((99,-55)).segment((-77,-55)).segment((-89,-21)).segment((-80,-21)).segment((-80,72)).segment((-95,75)).segment((-97,75)).segment((-97,74)).segment((-100,72)).close().assemble().finalize().extrude(75).union(w1.workplane(offset=72/2).moveTo(-69.5,-60.5).box(55,11,72))