import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-45))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((-11,-89),(11,-78),(27,-61)).close().assemble().reset().face(w0.sketch().segment((-11,61),(27,89)).arc((11,78),(-11,89)).close().assemble()).reset().face(w0.sketch().arc((30,-57),(40,-37),(44,-16)).segment((44,-14)).arc((40,-36),(30,-57)).assemble()).finalize().extrude(145).union(w1.sketch().segment((-27,-100),(-17,-100)).arc((0,-99),(17,-100)).segment((27,-100)).segment((27,-96)).arc((19,-98),(11,-99)).arc((-10,-98),(-27,-90)).close().assemble().finalize().extrude(-199))