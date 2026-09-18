import cadquery as cq
w0=cq.Workplane('YZ',origin=(-97,0,0))
w1=cq.Workplane('XY',origin=(0,0,66))
r=w0.sketch().arc((-86,-43),(-77,-36),(-68,-30)).arc((-23,59),(58,5)).arc((64,3),(69,0)).arc((-17,78),(-86,-43)).assemble().finalize().extrude(195).union(w1.sketch().segment((-97,-7),(-33,-7)).arc((-65,18),(-97,43)).close().assemble().finalize().extrude(-166))