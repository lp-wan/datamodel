import datetime



for td in range(55):
    dur = 2**td/10**6

    def print_date(val):
        sec = int(val)
        mu_sec = val-sec
        min = sec // 60
        sec = sec % 60

        hours = min // 60
        min = min % 60

        days = hours //24
        hours = hours % 24

        year = days//365
        days = days%365

        print ("{:05}y {:03}d {:02}h {:02}m {:02}s.{:06d}".format(year, days, hours, min, sec, int(mu_sec*1000_000)), end = "")

    print ("{:02}".format(td), end=" ")
    print_date(dur)    
    print ("<->", end="")
    print_date(dur*65535)
    print ()