class Player:
    def __init__(self, disc_data, disc_num_values, overall_bet, player_confirmed, player_balance, round_over, ready, id, player_bet, done, rev, has_bet):
        self.disc_data = disc_data
        self.disc_num_values = disc_num_values
        self.overall_bet = overall_bet
        self.player_confirmed = player_confirmed
        self.player_balance = player_balance
        self.player_bet = player_bet

        self.has_bet = has_bet

        self.rev = rev

        self.done = done

        self.id = id

        self.player_ready = ready
        self.round_over = round_over
