from sys import exit
if __name__ != "__main__": exit()


from EverburnLauncher.Library.EverburnBot import EverburnBot
from EverburnLauncher.Library.Dashboard import Dashboard

MainEvent:EverburnBot = EverburnBot()
MainEvent.Dashboard = Dashboard
MainEvent.Bot.run(MainEvent.Token)

MainEvent.Output("stopped")
exit()