import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().rect(60,36).rect(56,36,mode='s').finalize().extrude(-200).union(w0.sketch().segment((-30,-20),(20,-20)).segment((20,-8)).segment((30,-8)).segment((30,8)).segment((20,8)).segment((20,20)).segment((-30,20)).close().assemble().circle(23,mode='s').finalize().extrude(-198))