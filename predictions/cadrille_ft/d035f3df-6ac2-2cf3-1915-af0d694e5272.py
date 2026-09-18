import cadquery as cq
outer_length = 20.0
outer_length = 20.0
outer_length = 20.0
outer_length = 20.0
outer_length = 20.0
outer_length = 20.0
outer_length = 20.0
outer = cq.Workplane('XY').circle(2).circle(1,mode='s').finalize().extrude(-120).union(w0.sketch().segment((-62,35),(-58,-37)).segment((62,-36)).segment((58,37)).close().assemble().push([(25,-2)]).circle(5,mode='s').finalize().extrude(-100)).union(w0.sketch().segment((-54,-1),(-51,-1)).arc((-40,-34),(-10,-46)).segment((-10,-49)).segment((10,-49)).segment((10,-46)).arc((40,-34),(51,-1)).segment((54,-1)).segment((54,1)).segment((51,1)).arc((40,34),(10,46)).segment((10,49)).segment((-10,49)).segment((-10,46)).arc((-40,34),(-51,1)).segment((-54,1)).close().assemble().finalize().extrude(100))