import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,1))
r=w0.workplane(offset=-15/2).box(200,76,15).union(w0.sketch().segment((-38,-15),(38,-15)).segment((38,15)).segment((-38,15)).segment((-38,10)).arc((-37,9),(-38,8)).close().assemble().finalize().extrude(13))