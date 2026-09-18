import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
r=w0.sketch().circle(35).push([(8,0)]).circle(12,mode='s').finalize().extrude(-30).union(w0.sketch().segment((-43,-2),(-39,-19)).segment((-35,-18)).arc((10,-40),(42,-1)).segment((43,-1)).segment((39,16)).segment((38,16)).arc((-10,40),(-42,-1)).close().assemble().circle(35,mode='s').finalize().extrude(-1))
