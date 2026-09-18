import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,87))
w1=cq.Workplane('XY',origin=(0,0,88))
r=w0.sketch().segment((-97,-2),(-94,-2)).arc((0,-96),(94,-2)).segment((97,-2)).segment((97,6)).segment((94,6)).arc((0,96),(-94,6)).segment((-97,6)).close().assemble().push([(0,-1)]).circle(88,mode='s').finalize().extrude(-148).union(w1.sketch().push([(0,-1)]).circle(88).push([(-79,16)]).circle(13,mode='s').finalize().extrude(-188))