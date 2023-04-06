class Player:
    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
        self.highest_score_greek = 0
        self.highest_score_roman = 0
        self.highest_score_norse = 0
        self.highest_score_combined = 0
        self.profile_pic = ""
