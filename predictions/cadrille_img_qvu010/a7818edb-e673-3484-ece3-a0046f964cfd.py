import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-24,0))
w1=cq.Workplane('YZ',origin=(91,0,0))
r=w0.sketch().segment((-100,-100),(-95,-100)).segment((-100,-93)).close().assemble().reset().face(w0.sketch().segment((-100,-89),(100,89)).segment((-100,89)).close().assemble()).reset().face(w0.sketch().segment((-100,89),(100,89)).arc((0,100),(-100,89)).assemble()).finalize().extrude(54).union(w1.sketch().arc((-98,10),(-89,-1),(-83,-13)).arc((-79,-16),(-80,-21)).arc((-79,-54),(-58,-81)).arc((78,29),(-98,10)).assemble().finalize().extrude(-183))