import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-35,0))
w1=cq.Workplane('YZ',origin=(92,0,0))
r=w0.sketch().push([(33,23)]).circle(15).circle(11,mode='s').finalize().extrude(10).union(w1.sketch().arc((-83,-91),(-79,-92),(-74,-93)).segment((-74,-91)).segment((74,-91)).segment((74,-93)).arc((80,-92),(83,-91)).arc((68,0),(83,91)).arc((80,92),(74,93)).segment((74,91)).arc((0,80),(-74,91)).segment((-74,93)).arc((-80,92),(-83,91)).segment((-74,91)).segment((-74,-91)).close().assemble().finalize().extrude(-151))