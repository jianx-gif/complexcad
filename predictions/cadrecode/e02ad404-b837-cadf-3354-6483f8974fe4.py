import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().segment((-99,-20),(-97,-22)).arc((-67,-73),(-13,-99)).segment((-11,-100)).segment((-10,-99)).arc((73,-67),(97,19)).segment((99,20)).segment((97,22)).arc((67,73),(13,99)).segment((11,100)).segment((10,99)).arc((-73,67),(-97,-19)).close().assemble().circle(58,mode='s').finalize().extrude(-16)