parts = [base]
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-12, -10, 2.5), seat=2.5, flip=False))
parts.append(place(fastener("heatset", 'M4', 1), axis=(0, 0, 1), point=(-12, -10, 2.5), seat=3.4, flip=False))
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-12, -10, 2.5), seat=-2.5, flip=True))
