import cadquery as cq
w0=cq.Workplane('YZ',origin=(-42,0,0))
w1=cq.Workplane('XY',origin=(0,0,6))
r=w0.sketch().segment((-36,-17),(-23,-22)).segment((-15,-3)).segment((-28,2)).close().assemble().finalize().extrude(16).union(w0.sketch().push([(-24,0)]).circle(12).circle(6,mode='s').finalize().extrude(84)).union(w1.workplane(offset=-13/2).box(200,100,13))