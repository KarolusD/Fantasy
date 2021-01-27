class Player:
    def __init__(
        self, player_name,
        player_team,
        player_position,
        player_cost,
        player_selected_by,
        player_form,
        player_total_points
    ):
        self.player_name = player_name
        self.player_team = player_team
        self.player_position = player_position
        self.player_cost = player_cost
        self.player_selected_by = player_selected_by
        self.player_form = player_form
        self.player_total_points = player_total_points
