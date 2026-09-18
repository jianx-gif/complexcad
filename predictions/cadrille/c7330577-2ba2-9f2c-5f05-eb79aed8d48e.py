import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-64))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().push([(-4,0)]).circle(96).circle(83,mode='s').finalize().extrude(128).union(w1.sketch().arc((-19,-11),(-17,0),(-19,11)).close().assemble().finalize().extrude(-186))