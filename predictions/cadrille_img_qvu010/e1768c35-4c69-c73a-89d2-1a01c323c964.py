import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-43,0))
w1=cq.Workplane('YZ',origin=(-81,0,0))
r=w0.sketch().arc((-35,-29),(0,3),(35,-29)).arc((0,44),(-35,-29)).assemble().finalize().extrude(-56).union(w0.sketch().arc((-100,69),(-73,79),(-45,83)).arc((19,76),(72,41)).arc((85,1),(82,-41)).arc((89,-49),(90,-59)).arc((98,-37),(100,-14)).segment((87,-14)).segment((87,59)).segment((100,59)).arc((0,92),(-100,59)).close().assemble().finalize().extrude(125)).union(w1.sketch().arc((14,-99),(57,-57),(14,-15)).segment((14,-23)).arc((45,-57),(14,-92)).close().assemble().finalize().extrude(111))