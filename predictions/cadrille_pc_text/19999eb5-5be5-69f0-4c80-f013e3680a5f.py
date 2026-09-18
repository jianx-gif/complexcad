import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-2))
w1=cq.Workplane('YZ',origin=(-82,0,0))
r=w0.workplane(offset=-9/2).moveTo(-91,0).box(18,174,9).union(w1.sketch().segment((-58,-11),(58,-11)).segment((58,11)).segment((-58,11)).segment((-58,9)).arc((-55,7),(-58,5)).close().assemble().rect(24,18,mode='s').finalize().extrude(182))