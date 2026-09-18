import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,14,0))
w1=cq.Workplane('YZ',origin=(-24,0,0))
r=w0.sketch().segment((-75,47),(-36,-47)).arc((-36,10),(-75,47)).assemble().finalize().extrude(-74).union(w0.sketch().push([(0,24)]).circle(58).push([(59,29)]).circle(33,mode='s').finalize().extrude(-11)).union(w0.sketch().segment((-28,-39),(-27,-40)).segment((28,39)).segment((27,40)).close().assemble().finalize().extrude(83)).union(w1.sketch().arc((-30,100),(-10,7),(30,95)).arc((29,97),(28,100)).close().assemble().finalize().extrude(124))