parts = [base]
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-35, 0, 4), seat=10, flip=False))
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-35, 0, 4), seat=11.5, flip=False))
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(35, 0, 4), seat=10, flip=False))
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-35, 0, 4), seat=-4, flip=True))
