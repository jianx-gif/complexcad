import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
w1=cq.Workplane('YZ',origin=(-1,0,0))
r=w0.sketch().arc((-68,-36),(-34,-59),(7,-64)).segment((7,-51)).segment((20,-51)).segment((20,-57)).arc((44,-37),(58,-9)).arc((59,2),(68,10)).arc((34,59),(-27,64)).close().assemble().finalize().extrude(200).union(w1.sketch().push([(-10,0)]).circle(90).circle(85,mode='s').finalize().extrude(-90))