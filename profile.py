class Profile:
    """ Profile represents a person with their name, wins, losses and position on the leaderboard
    """   

    def __init__(self, name: str) -> None:
        """ initializes rank
        >>> h = Profile(Hayden)
        """
        self.__name = name
        self.__rank = 0#placeholder for the rank fuction
        self.__wins = 0
        self.__losses = 0

    def get_rank(self)->int:
      """
      """
