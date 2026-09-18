import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,1,0))
w1=cq.Workplane('ZX',origin=(0,-10,0))
r=w0.sketch().push([(0,23)]).circle(70).push([(-41,26)]).circle(20,mode='s').push([(76,29)]).circle(15,mode='s').finalize().extrude(-58).union(w0.sketch().segment((-59,32),(59,32)).arc((0,65),(-59,32)).assemble().finalize().extrude(56)).union(w1.sketch().arc((-100,-20),(19,23),(100,-60)).segment((100,39)).arc((19,65),(-59,36)).segment((-59,92)).segment((-100,92)).close().assemble().finalize().extrude(-6))