import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-95))
w1=cq.Workplane('YZ',origin=(-45,0,0))
r=w0.sketch().arc((-45,-65),(-39,-59),(-32,-54)).arc((-39,-57),(-45,-61)).close().assemble().finalize().extrude(191).union(w1.sketch().arc((35,59),(-39,-46),(48,49)).arc((53,54),(58,58)).arc((-50,-81),(41,68)).arc((37,64),(35,59)).assemble().finalize().extrude(145))