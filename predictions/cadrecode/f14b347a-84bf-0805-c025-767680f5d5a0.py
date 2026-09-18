import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,12))
w1=cq.Workplane('XY',origin=(0,0,13))
r=w0.sketch().segment((-48,-81),(-10,-81)).segment((-10,-75)).segment((-48,-75)).segment((-48,-76)).segment((-47,-76)).segment((-47,-78)).segment((-48,-78)).close().assemble().finalize().extrude(-24).union(w1.sketch().segment((-50,-95),(-47,-95)).segment((-47,-100)).segment((50,-100)).segment((50,-75)).segment((10,-75)).arc((0,-86),(-10,-75)).segment((-25,-75)).segment((-25,100)).segment((-50,100)).close().assemble().push([(-46.5,-41.5)]).rect(3,5,mode='s').finalize().extrude(-26))