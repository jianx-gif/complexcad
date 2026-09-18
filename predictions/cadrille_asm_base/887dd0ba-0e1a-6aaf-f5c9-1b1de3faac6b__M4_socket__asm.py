import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-23))
w1=cq.Workplane('XY',origin=(0,0,-8))
r=w0.sketch().segment((77,16),(86,14)).segment((92,23)).segment((77,33)).close().assemble().finalize().extrude(34).union(w0.sketch().circle(16).circle(9,mode='s').finalize().extrude(47)).union(w1.sketch().segment((-100,-33),(-9,-33)).segment((-9,-22)).segment((9,-22)).segment((9,-33)).segment((100,-33)).segment((100,33)).segment((9,33)).segment((9,-22)).segment((-9,-22)).segment((-9,33)).segment((-100,33)).close().assemble().finalize().extrude(11))