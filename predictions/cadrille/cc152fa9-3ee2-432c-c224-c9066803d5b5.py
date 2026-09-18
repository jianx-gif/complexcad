import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
w1=cq.Workplane('ZX',origin=(0,0,0))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-72,-20),(43,-67)).segment((72,20)).segment((-43,67)).close().assemble(),mode='s').finalize().extrude(-15).union(w0.sketch().circle(52).push([(35,-11)]).circle(19,mode='s').finalize().extrude(-3)).union(w1.sketch().segment((-25,-20),(25,-20)).segment((25,-1)).arc((0,-15),(-25,-1)).close().assemble().finalize().extrude(6))