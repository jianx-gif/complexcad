import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-38,-21),(-34,-24)).segment((34,-24)).segment((38,-21)).segment((37,-21)).segment((37,27)).segment((34,29)).segment((11,29)).segment((7,26)).segment((7,-7)).segment((-34,-9)).close().assemble().finalize().extrude(-200)