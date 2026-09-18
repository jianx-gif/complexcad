import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-38,-25),(-25,-25)).arc((0,-38),(25,-25)).segment((38,-25)).segment((38,25)).segment((25,25)).arc((0,38),(-25,25)).segment((-38,25)).close().assemble().circle(30,mode='s').finalize().extrude(-200)