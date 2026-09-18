import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().circle(100).circle(97,mode='s').circle(70).finalize().extrude(-200).union(w0.sketch().arc((-83,-5),(-45,-53),(14,-70)).segment((14,-68)).segment((18,-68)).segment((18,-70)).arc((57,-55),(83,-23)).arc((38,12),(35,71)).arc((-36,61),(-80,7)).arc((-81,2),(-83,-5)).assemble().finalize().extrude(-195))