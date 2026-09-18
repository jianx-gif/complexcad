import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-36))
w1=cq.Workplane('YZ',origin=(43,0,0))
r=w0.sketch().push([(-11,0)]).circle(57).circle(43,mode='s').circle(29).finalize().extrude(136).union(w1.sketch().arc((-48,-79),(-10,-100),(29,-79)).close().assemble().finalize().extrude(-81))