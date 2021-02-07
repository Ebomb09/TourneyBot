import doctest

class Profile:
    """ Profile represents a person with their name, wins, losses and rank
    """   

    def __init__(self, name: str, i_d: int) -> None:
        """Initializes a profile with name, id, , wins, losses
        >>> h = Profile('Hayden', 51)
        """
        self.__name = name
        self.__id = i_d
        self.__wins = 0
        self.__losses = 0

        """
        def get_rank(self)->int:
        Returns the user's rank
        >>> h = Profile('Hayden', 51)
        >>> h.get_rank()
        1
        
        return self.__rank
        """
    def get_wins(self)->int:
        """Returns the user's wins
        >>> h = Profile('Hayden', 51)
        >>> h.get_wins()
        0
        """
        return self.__wins

    def get_losses(self)->int:
        """Returns the user's losses
        >>> h = Profile('Hayden', 51)
        >>> h.get_losses()
        0
        """
        return self.__losses    
    
    def get_name(self)->str:
        """Returns the user's name
        >>> h = Profile('Hayden', 51)
        >>> h.get_name()
        'Hayden'
        """
        return self.__name      
    
    def get_id(self)->int:
        """Returns the user's id
        >>> h = Profile('Hayden', 51)
        >>> h.get_id()
        51
        """
        return self.__id    
    
    def add_win(self)->None:
        """Adds 1 to the win total
        >>> h = Profile('Hayden', 51)
        >>> h.add_win()
        >>> h.get_wins()
        1
        """
        self.__wins += 1
    
    def add_loss(self)->None:
        """Adds 1 to the loss total
        >>> h = Profile('Hayden', 51)
        >>> h.add_loss()
        >>> h.get_losses()
        1
        """
        self.__losses += 1    
   