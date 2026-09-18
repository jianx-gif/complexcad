import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-14))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(14).push([(4,-2)]).circle(8,mode='s').finalize().extrude(43).union(w0.sketch().segment((2,5),(8,5)).arc((5,6),(2,5)).assemble().finalize().extrude(114)).union(w1.sketch().segment((-9,-8),(-8,-8)).segment((-8,-11)).segment((8,-11)).segment((8,-8)).segment((9,-8)).segment((9,-1)).segment((8,-1)).segment((8,0)).segment((-8,0)).segment((-8,-1)).segment((-9,-1)).close().assemble().finalize().extrude(200))