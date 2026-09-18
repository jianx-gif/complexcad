import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-14,0))
w1=cq.Workplane('XY',origin=(0,0,-53))
r=w0.sketch().push([(0,-1)]).rect(200,188).reset().face(w0.sketch().segment((-59,-66),(59,-66)).segment((59,-47)).arc((0,-65),(-59,-47)).close().assemble(),mode='s').reset().face(w0.sketch().arc((-59,47),(0,65),(59,47)).segment((59,66)).segment((-59,66)).close().assemble(),mode='s').push([(84,26)]).circle(12,mode='s').finalize().extrude(21).union(w1.sketch().arc((1,-89),(29,0),(1,89)).close().assemble().finalize().extrude(109))