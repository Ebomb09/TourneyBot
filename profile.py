from leaderboard import Leaderboard

class Profile:
    """ Profile represents a person with their name, wins, losses and rank
    """   

    def __init__(self, name: str, i_d: int, board: Leaderboard) -> None:
        """ 
        >>> h = Profile(Hayden, 51, main_board)
        """
        self.__name = name
        self.__id = i_d
        self.__rank = board.new_pro(self)
        self.__wins = 0
        self.__losses = 0

    def get_rank(self)->int:
      """
      """
