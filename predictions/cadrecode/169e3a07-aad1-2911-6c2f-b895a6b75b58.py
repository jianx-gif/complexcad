import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,53))
w1=cq.Workplane('XY',origin=(0,0,47))
r=w0.sketch().circle(100).reset().face(w0.sketch().segment((-95,-29),(-74,-37)).arc((-32,-73),(22,-77)).segment((43,-85)).segment((52,-60)).arc((73,-33),(80,1)).segment((95,29)).segment((74,37)).arc((32,73),(-22,77)).segment((-43,85)).segment((-52,60)).arc((-73,33),(-80,-1)).close().assemble(),mode='s').finalize().extrude(-106).union(w1.sketch().circle(96).circle(96,mode='s').finalize().extrude(-99))