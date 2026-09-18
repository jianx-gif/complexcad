import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().segment((-16,-72),(-10,-72)).segment((-10,-80)).segment((6,-80)).segment((6,80)).segment((-10,80)).segment((-10,-64)).segment((-16,-64)).close().assemble().push([(1,-17)]).circle(3,mode='s').finalize().extrude(-200).union(w0.sketch().segment((-56,-20),(-56,20)).arc((-59,0),(-56,-20)).assemble().finalize().extrude(-132))