import cadquery as cq
w0=cq.Workplane('YZ',origin=(-93,0,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-53,-38),(53,-38)).segment((53,38)).segment((-53,38)).segment((-53,3)).arc((-47,-1),(-53,-5)).close().assemble().rect(94,70,mode='s').finalize().extrude(193).union(w1.sketch().segment((-51,-38),(-46,-38)).segment((-46,-42)).segment((46,-42)).segment((46,-38)).segment((51,-38)).segment((51,38)).segment((46,38)).segment((46,42)).segment((-46,42)).segment((-46,38)).segment((-51,38)).close().assemble().rect(52,70,mode='s').finalize().extrude(200))