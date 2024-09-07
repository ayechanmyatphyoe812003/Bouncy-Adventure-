class Data:
    def __init__(self, ui):
        self.ui = ui  # Stores the UI object, which will be used to update the user interface
        self._coins = 0  # Initializes the private attribute _coins to 0
        self._health = 5  # Initializes the private attribute _health to 5
        self.ui.create_hearts(self._health)  # Updates the UI to display the initial number of health hearts

        self._unlocked_level = 0  # Initializes the unlocked_level attribute to 0.
        # This tracks the highest level unlocked by the player

        self.current_level = 0  # Initializes the current_level attribute to 0.
        # This tracks the level currently being played
        self.ui = ui
        self.ui.update_unlocked_level(self._unlocked_level)
        # self.update_ui()

    @property
    def unlocked_level(self):
        return self._unlocked_level

    @unlocked_level.setter
    def unlocked_level(self, value):
        self._unlocked_level = value
        self.ui.update_unlocked_level(value)

    @property
    def health(self):
        # print('health was read')
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        self.ui.create_hearts(value)  # Updates the UI to display

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, value):
        self._coins = value
        if self.coins >= 100:
            self.coins -= 100
            self.health += 1
        self.ui.show_coins(self.coins)  # Updates the UI to display
