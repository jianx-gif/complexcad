import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().push([(-87.5,0)]).rect(25,150).push([(18.5,-62.5)]).rect(163,25).push([(-50,-63)]).circle(7,mode='s').push([(50,-64)]).circle(7,mode='s').finalize().extrude(-25)