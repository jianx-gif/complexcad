import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-45))
r=w0.sketch().segment((-30,-20),(30,-20)).segment((30,-10)).arc((58,40),(30,89)).segment((30,100)).segment((-30,100)).segment((-30,89)).arc((-58,40),(-30,-10)).close().assemble().finalize().extrude(12).union(w0.sketch().push([(0,-10)]).circle(90).push([(-85,1)]).circle(3,mode='s').finalize().extrude(90))