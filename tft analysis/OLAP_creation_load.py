import tft_utils.py as tft

def load_set_data():
    '''
    in order to do proper data analysis it is important that we track
    no only tft match data but the data about the champions used themselves.
    This is static information about the game that does not change from match
    to match and will be used to organize the analytical tool better
    '''
    TftDataUrl = "https://raw.communitydragon.org/latest/cdragon/tft/en_us.json"
    TftRequestData = requests.get(TftDataUrl)
    TftData = TftRequestData.json()
    Setdata = TftData['setData']
    ItemData = TftData['items']
    Items = ItemData[]


def initial_load():
    '''
    This function will be the initial load for the tft dataset.
    This will be designed to work for any tft set and will create the
    tables needed then populate the dataset with the minimum needed

    this is a mongodb no sql database that will store the match information

    a sql relational database to keep track of additions to the database

    for incremental loads.

    the database will have a match first philosophy and will only analyze matches
    in which atleast one player is in challenger,master or grandmaster at ome point this patch

    as in if player x was grandmaster when we first analyze their matches this tft
    set then we will as much of their match history as we desire into the set regardless of
    what their rank is

    this is done for two reasons, one being how tft matches are stored on the league server. In order to get
    a match we must get a set of players from a particular rank and then get their match history.
    we cannot get the rank of players at the time of the match therefore we will only analyze matches from high level players
    and assume that they are making decent decisions

    we will look at na,kr,jp matches    
    '''
    na = tft.Region.North_America.value
    jp = tft.Region.Japan.value
    kr = tft.Region.Republic_Korea
    
    na_players = tft.get_players_by_rank(tft.Rank.
def incremental_load():
    pass
