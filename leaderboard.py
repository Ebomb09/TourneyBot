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

  def new_profile(self, per: Profile)->None:
    """Adds a new profile to the leaderboard
    >>> ldr = Leaderboard()
    >>> h = Profile('Hayden', 51)
    >>> ldr.new_profile(h)
    """
    self.__rankings.append(per)
    self.__total += 1
    
  def get_rank(self, per: Profile)->int:
    """Return the rank of the given person on the leaderboard
    >>> ldr = Leaderboard()
    >>> h = Profile('Hayden', 51)
    >>> ldr.new_profile(h)
    >>> d = Profile('Kayden', 31)
    >>> ldr.new_profile(d)
    >>> ldr.get_rank(h)
    1
    >>> ldr.get_rank(d)
    2
    """
    result = 1
    for index in range(len(self.__rankings)):
      if per == self.__rankings[index]:
        return result
      result += 1
      
  def update_ranks(self, per1: Profile, per2: Profile)->None:
    """take two profile and switches their ranks
    >>> ldr = Leaderboard()
    >>> h = Profile('Hayden', 51)
    >>> ldr.new_profile(h)
    >>> d = Profile('Kayden', 31)
    >>> ldr.new_profile(d)
    >>> ldr.update_ranks(h,d)
    >>> ldr.get_rank(h)
    2
    >>> ldr.get_rank(d)
    1
    """
    x = self.get_rank(per1)
    y = self.get_rank(per2)
    self.__rankings[x-1] = per2
    self.__rankings[y-1] = per1
    