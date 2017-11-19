from postern.dotnet import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('AdWindows')

import Autodesk.Revit.DB as DB
import Autodesk.Revit.UI as UI
import Autodesk.Windows as AdWindows
