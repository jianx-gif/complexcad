import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-7))
w1=cq.Workplane('XY',origin=(0,0,-16))
r=w0.sketch().segment((88,-36),(100,-36)).segment((100,36)).segment((88,36)).segment((88,2)).arc((91,-1),(88,-4)).close().assemble().finalize().extrude(23).union(w1.sketch().push([(-6,0)]).rect(188,118).push([(-6,-0.5)]).rect(170,99,mode='s').finalize().extrude(28))