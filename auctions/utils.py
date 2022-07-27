



def valid_bid(bid, new):
    for s in bid:
        if int(s.bid) >= int(new):
            return False
    return True

