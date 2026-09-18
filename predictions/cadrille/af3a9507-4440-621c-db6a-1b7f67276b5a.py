import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-38,-31),(38,-31)).arc((0,31),(-38,-31)).assemble().push([(4,-1)]).circle(25,mode='s').finalize().extrude(-200).union(w0.workplane(offset=-198/2).box(36,48,198))