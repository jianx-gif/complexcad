import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-6))
r=w0.sketch().segment((-100,-66),(-93,-66)).segment((-93,-75)).segment((98,-75)).segment((98,-66)).segment((100,-66)).segment((100,-38)).segment((-62,-38)).segment((-62,75)).segment((-100,75)).close().assemble().finalize().extrude(-38).union(w0.workplane(offset=50/2).moveTo(-81,-56).box(30,30,50))