import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().segment((-100,-52),(-99,-52)).segment((-99,-67)).segment((99,-67)).segment((99,-52)).segment((100,-52)).segment((100,52)).segment((99,52)).segment((99,67)).segment((-99,67)).segment((-99,52)).segment((-100,52)).close().assemble().circle(53,mode='s').finalize().extrude(-26)