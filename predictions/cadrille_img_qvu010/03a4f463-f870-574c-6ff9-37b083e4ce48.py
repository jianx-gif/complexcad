import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-16,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().push([(0,-1)]).circle(14).circle(10,mode='s').finalize().extrude(10).union(w0.sketch().segment((-80,-11),(80,11)).arc((-1,42),(-80,-11)).assemble().finalize().extrude(107)).union(w1.sketch().segment((-90,-21),(-70,-21)).segment((-70,-27)).segment((-1,-27)).segment((-1,-90)).arc((27,-63),(50,-27)).segment((70,-27)).segment((70,-21)).segment((90,-21)).segment((90,-18)).segment((-90,-18)).close().assemble().finalize().extrude(-200))