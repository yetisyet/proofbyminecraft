class WorldGen:
    def __init__(self):
        pass

    def Write():
        file = open("data/r.0.0.mca", "wb", newline=None)

        out_bytes = []

        timestamps = bytes([0 for i in range(4096)])
        out_bytes.extend(timestamps)

        print(f"write size: {len(out_bytes)}")

        file.write(bytes(out_bytes))

        file.close()