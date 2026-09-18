import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-1))
r=w0.sketch().segment((-87,-8),(-19,-8)).segment((-19,-84)).segment((19,-84)).segment((19,-8)).segment((87,-8)).segment((87,8)).segment((19,8)).segment((19,84)).segment((-19,84)).segment((-19,8)).segment((-87,8)).close().assemble().finalize().extrude(-16).union(w0.sketch().circle(100).circle(23,mode='s').finalize().extrude(18))