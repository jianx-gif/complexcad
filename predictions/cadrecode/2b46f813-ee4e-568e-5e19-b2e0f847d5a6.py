import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,37))
w1=cq.Workplane('XY',origin=(0,0,48))
r=w0.sketch().segment((-26,-98),(-18,-100)).segment((-15,-89)).arc((49,-35),(22,42)).segment((26,53)).segment((18,55)).segment((15,45)).arc((-91,6),(-22,-89)).close().assemble().push([(-21,-16)]).circle(66,mode='s').finalize().extrude(-91).union(w0.sketch().push([(0,5)]).circle(95).push([(0,5.5)]).rect(154,77,mode='s').finalize().extrude(18)).union(w1.sketch().push([(-21,-16)]).circle(62).push([(-21,-16.5)]).rect(106,11,mode='s').finalize().extrude(-94))