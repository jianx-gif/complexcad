import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,29))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().circle(14).push([(1,10)]).circle(5,mode='s').finalize().extrude(-53).union(w1.sketch().segment((-9,-11),(8,-11)).segment((8,-10)).segment((9,-10)).segment((9,0)).segment((8,0)).segment((8,1)).segment((-9,1)).close().assemble().finalize().extrude(-200))