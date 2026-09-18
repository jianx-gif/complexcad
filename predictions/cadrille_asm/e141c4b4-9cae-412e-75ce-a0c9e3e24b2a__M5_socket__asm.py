parts = [base]
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-10, -10, 2.5), seat=2.5, flip=False))
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-10, -10, 2.5), seat=3.4, flip=False))
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(10, -10, 2.5), seat=2.5, flip=False))
parts.append(place(fastener("washer", 'M4', 1), axis=(0, 0, 1), point=(25, -10, 2.5), seat=3.4, flip=False))
