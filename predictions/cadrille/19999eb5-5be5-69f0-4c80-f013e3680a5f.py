import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-2))
w1=cq.Workplane('YZ',origin=(-82,0,0))
r=w0.sketch().push([(-91,0)]).rect(18,174).push([(-91.5,0)]).rect(13,10,mode='s').finalize().extrude(-9).union(w1.sketch().segment((-58,-11),(58,-11)).segment((58,11)).segment((-58,11)).segment((-58,9)).segment((-11,9)).segment((-11,-9)).segment((-58,-9)).close().assemble().push([(34,-1)]).rect(42,16,mode='s').finalize().extrude(182))