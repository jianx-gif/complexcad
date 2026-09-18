import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-90,-1),(-67,-1)).arc((0,-67),(67,-1)).segment((90,-1)).segment((90,1)).segment((67,1)).arc((0,67),(-67,1)).segment((-90,1)).close().assemble(),mode='s').push([(4.5,-87.5)]).rect(3,1,mode='s').push([(4.5,87.5)]).rect(3,1,mode='s').finalize().extrude(-16)