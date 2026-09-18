import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-69,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-66,-60),(-66,-53)).arc((-62,-57),(-57,-61)).segment((-64,-61)).arc((0,-86),(64,-61)).segment((57,-61)).arc((62,-57),(66,-53)).segment((66,-60)).arc((86,0),(66,60)).segment((66,53)).arc((62,57),(57,61)).segment((64,61)).arc((0,86),(-64,61)).segment((-57,61)).arc((-62,57),(-66,53)).segment((-66,60)).arc((-86,0),(-66,-60)).assemble().circle(78,mode='s').finalize().extrude(13).union(w1.sketch().circle(86).circle(84,mode='s').finalize().extrude(200))