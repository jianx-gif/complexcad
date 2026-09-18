import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-30,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((-45,-59),(47,-69),(100,5)).segment((83,-15)).arc((75,-32),(61,-45)).segment((45,-65)).segment((35,-57)).arc((-10,-55),(-45,-30)).close().assemble().finalize().extrude(120).union(w1.sketch().push([(-20.5,0)]).rect(159,200).push([(-21,0)]).circle(89,mode='s').finalize().extrude(-174))