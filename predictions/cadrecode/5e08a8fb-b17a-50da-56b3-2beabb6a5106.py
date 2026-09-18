import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,37))
r=w0.sketch().segment((-100,-58),(-95,-58)).segment((-95,-63)).segment((95,-62)).segment((95,-58)).segment((100,-58)).segment((100,58)).segment((95,58)).segment((95,62)).segment((-95,62)).segment((-95,58)).segment((-100,58)).close().assemble().circle(10,mode='s').finalize().extrude(-75)