years : list[str] = ['2017','2018','2019','2020','2021','2022'] #defaults to ['2017','2018','2019','2020','2021','2022']
dataType : list[str] = ['operating','revenue'] #defaults to ['operating','revenue']
scrollTimeOut : int = 3 # Do not fuck with this. Milliseconds between scrolls
pixelScroll  : int = 15 # Do not fuck with this. How many pixels are scroll per scrollTimeOut milliseconds
processors  : int = 2 # recommend no higher than the number of cores on your PC
depthRevenue : int = 2 #max data at 5
depthExpense : int = 2 #max data at 3
numSample  : int = 4 # testing purposes only

#cities : list[str] = ['Los Angeles', "Sacramento"] TODO: !Not Implemented: Check back for the newest version on Github
#keywords : list[str] = ['police', 'fire']  TODO: !Not Implemented: Check back for the newest version on Github