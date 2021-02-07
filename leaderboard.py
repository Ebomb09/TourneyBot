from profile import Profile
import doctest

class Leaderboard:
  """Leaderboard stores profiles by rank, the number of profiles in the leaderboard
  """
  def __init__(self) -> None:
    """Itializes a Leaderboard
    >>> ldr = Leaderboard()
    """
    self.__rankings = []
    self.__total = 0

  def new_pro(self, per: Profile)->int:
    """Adds a new profile to the leaderboard and returns the rank given
    >>> ldr = Leaderboard()
    >>> h = Profile(Hayden)
    >>> ldr.new_pro(h)
    1
    """
    self.__rankings[self.__total] = per
    self.__total += 1
    return self.__total
