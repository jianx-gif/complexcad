import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,67))
w1=cq.Workplane('XY',origin=(0,0,76))
r=w0.sketch().circle(77).push([(13,0)]).circle(7,mode='s').finalize().extrude(-155).union(w0.sketch().segment((-62,-16),(-51,-16)).arc((0,-54),(51,-16)).segment((62,-16)).segment((62,16)).segment((51,16)).arc((0,54),(-51,16)).segment((-62,16)).close().assemble().finalize().extrude(22)).union(w1.sketch().circle(31).push([(13,0)]).circle(8,mode='s').finalize().extrude(-176))