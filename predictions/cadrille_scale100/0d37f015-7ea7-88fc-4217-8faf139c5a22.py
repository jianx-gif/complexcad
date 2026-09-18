import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('YZ',origin=(11,0,0))
r=w0.sketch().segment((-21,-3),(-8,-18)).segment((21,3)).segment((8,18)).close().assemble().finalize().extrude(-20).union(w0.sketch().circle(30).circle(22,mode='s').finalize().extrude(10)).union(w0.workplane(offset=60/2).cylinder(60,20)).union(w1.sketch().arc((-16,-17),(-14,-17),(-13,-19)).arc((14,17),(-16,-17)).assemble().finalize().extrude(-33))