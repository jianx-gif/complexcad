import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().segment((-100,53),(-80,11)).arc((-6,18),(53,-33)).segment((55,-33)).segment((55,-67)).segment((100,-67)).arc((37,47),(-100,53)).assemble().finalize().extrude(-26)