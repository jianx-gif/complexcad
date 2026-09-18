import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-94,-1),(-67,-1)).arc((-4,-66),(65,-10)).segment((92,-10)).segment((92,1)).segment((66,1)).arc((1,67),(-67,1)).segment((-94,1)).close().assemble(),mode='s').push([(-1,-87)]).circle(4,mode='s').finalize().extrude(-16)