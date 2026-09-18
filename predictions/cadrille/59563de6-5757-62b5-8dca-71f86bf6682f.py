import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-47))
w1=cq.Workplane('XY',origin=(0,0,-92))
r=w0.sketch().segment((-56,-5),(-51,-5)).arc((0,-52),(51,-5)).segment((56,-5)).segment((56,5)).segment((51,5)).arc((0,52),(-51,5)).segment((-56,5)).close().assemble().circle(41,mode='s').finalize().extrude(69).union(w0.sketch().circle(43).circle(32,mode='s').finalize().extrude(147)).union(w1.sketch().arc((-40,12),(-48,-1),(-38,-13)).arc((48,10),(-40,12)).assemble().circle(41,mode='s').finalize().extrude(-8))