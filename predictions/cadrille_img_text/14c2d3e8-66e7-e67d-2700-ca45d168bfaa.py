import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-33,0))
w1=cq.Workplane('YZ',origin=(99,0,0))
r=w0.sketch().push([(0,12)]).rect(100,140).circle(33,mode='s').push([(71,-41)]).circle(13,mode='s').finalize().extrude(33).union(w0.sketch().push([(0,12)]).circle(11).circle(9,mode='s').finalize().extrude(112)).union(w1.sketch().arc((-87,-39),(0,-91),(87,-39)).segment((86,-39)).arc((80,-41),(74,-39)).close().assemble().finalize().extrude(-178))