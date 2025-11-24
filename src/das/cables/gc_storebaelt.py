from das.cables.cable import Cable


class GCStorebaelt(Cable):
    CABLE_RESOURCE = "cable_position.json"

    def __init__(self):
        super().__init__()
