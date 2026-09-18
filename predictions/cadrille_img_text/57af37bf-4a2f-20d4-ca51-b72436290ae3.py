import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('ZX',origin=(0,26,0))
r=w0.sketch().arc((-45,-69),(-20,-83),(8,-88)).segment((8,-90)).segment((13,-90)).segment((13,-88)).arc((55,-77),(88,-49)).segment((85,-49)).arc((5,-82),(-45,-69)).assemble().reset().face(w0.sketch().segment((-45,49),(-42,49)).arc((5,82),(52,49)).segment((55,49)).arc((5,84),(-45,49)).assemble()).finalize().extrude(200).union(w1.sketch().arc((35,-59),(38,-57),(41,-54)).segment((35,-54)).close().assemble().finalize().extrude(-103))