import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,1))
r=w0.workplane(offset=-15/2).box(200,76,15).union(w0.sketch().circle(38).push([(26,-1)]).circle(3,mode='s').finalize().extrude(13))