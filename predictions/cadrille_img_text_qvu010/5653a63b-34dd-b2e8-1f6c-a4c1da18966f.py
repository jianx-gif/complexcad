import cadquery as cq
w0=cq.Workplane('YZ',origin=(-98,0,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().circle(87).push([(25,29)]).circle(41,mode='s').finalize().extrude(177).union(w1.sketch().arc((-69,-73),(66,75),(-62,-78)).segment((-59,-78)).arc((66,75),(-69,-71)).close().assemble().finalize().extrude(200))