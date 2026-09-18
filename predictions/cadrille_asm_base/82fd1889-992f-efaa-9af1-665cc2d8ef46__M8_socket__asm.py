import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-65,0))
w1=cq.Workplane('YZ',origin=(31,0,0))
r=w0.sketch().segment((-28,1),(-6,-31)).segment((28,-1)).segment((6,31)).close().assemble().finalize().extrude(10).union(w0.workplane(offset=78/2).cylinder(78,25)).union(w0.workplane(offset=165/2).moveTo(0,-1).cylinder(165,21)).union(w1.sketch().push([(-82,0)]).circle(12).circle(8,mode='s').finalize().extrude(-62))