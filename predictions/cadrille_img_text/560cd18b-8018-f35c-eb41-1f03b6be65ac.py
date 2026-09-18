import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,5,0))
w1=cq.Workplane('YZ',origin=(89,0,0))
r=w0.sketch().arc((65,-59),(82,-52),(95,-39)).segment((74,-39)).close().assemble().finalize().extrude(-45).union(w0.sketch().push([(0,1)]).circle(59).circle(35,mode='s').finalize().extrude(-25)).union(w0.sketch().segment((-35,-49),(-34,-50)).segment((35,49)).segment((34,50)).close().assemble().finalize().extrude(85)).union(w1.sketch().arc((-55,-29),(-43,-27),(-31,-25)).arc((38,69),(1,-42)).arc((10,-65),(13,-89)).arc((41,49),(-55,-29)).assemble().finalize().extrude(-146))