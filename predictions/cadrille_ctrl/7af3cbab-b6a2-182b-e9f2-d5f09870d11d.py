import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().segment((-40,-20),(-17,-20)).arc((-30,-16),(-40,-7)).close().assemble().finalize().extrude(-20).union(w0.sketch().segment((-37,15),(-11,15)).arc((-24,20),(-37,15)).assemble().reset().face(w0.sketch().arc((-10,-19),(1,-19),(11,-15)).segment((37,-20)).segment((40,-1)).segment((14,3)).arc((12,11),(7,17)).arc((3,19),(-1,20)).arc((10,-3),(-10,-19)).assemble()).finalize().extrude(-20)).union(w0.sketch().push([(25,0)]).rect(30,40).push([(25.5,0)]).rect(15,2,mode='s').finalize().extrude(-20))
