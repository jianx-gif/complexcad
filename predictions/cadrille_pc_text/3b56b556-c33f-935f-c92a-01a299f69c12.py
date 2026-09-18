import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-12))
r=w0.workplane(offset=-10/2).moveTo(55,0).box(90,6,10).union(w0.sketch().push([(-31,0)]).rect(138,80).push([(-31,-1)]).rect(102,50,mode='s').finalize().extrude(13)).union(w0.sketch().segment((-100,-41),(38,-43)).segment((38,41)).segment((-100,43)).close().assemble().push([(-31,0)]).rect(104,52,mode='s').finalize().extrude(34))