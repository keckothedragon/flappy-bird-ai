class Movement:
    def __init__(self, delta_x: int, delta_y: int):
        self.delta_x = delta_x
        self.delta_y = delta_y

    def get_delta_x(self) -> int:
        return self.delta_x

    def get_delta_y(self) -> int:
        return self.delta_y

    def get_delta(self) -> tuple:
        return self.delta_x, self.delta_y
