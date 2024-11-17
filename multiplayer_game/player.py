class Player:
    def __init__(self, disc_data, disc_num_values, overall_bet, player_confirmed, player_balance, round_over, ready, id):
        self.disc_data = disc_data
        self.disc_num_values = disc_num_values
        self.overall_bet = overall_bet
        self.player_confirmed = player_confirmed
        self.player_balance = player_balance

        self.id = id

        self.player_ready = ready
        self.round_over = round_over
