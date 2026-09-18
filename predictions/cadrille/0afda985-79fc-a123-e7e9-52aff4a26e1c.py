import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,29))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(14).circle(6,mode='s').finalize().extrude(-45).union(w1.sketch().segment((-9,-11),(-8,-11)).segment((-8,-12)).segment((8,-12)).segment((8,-11)).segment((9,-11)).segment((9,1)).segment((8,1)).segment((8,2)).segment((2,2)).segment((2,6)).segment((8,6)).segment((8,11)).segment((9,11)).segment((9,12)).segment((8,12)).segment((8,13)).segment((-8,13)).segment((-8,12)).segment((-9,12)).close().assemble().finalize().extrude(-200))