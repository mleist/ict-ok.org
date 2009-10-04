
pdb in root view:

(Pdb) self.context
<zope.app.folder.folder.Folder object at 0x1fe9c70>

root=self.context

from org.ict_ok.components.location.interfaces import ILocation
from org.ict_ok.components.location.interfaces import ILocationFolder
from org.ict_ok.components.building.interfaces import IBuilding
from org.ict_ok.components.building.interfaces import IBuildingFolder
from org.ict_ok.components.room.interfaces import IRoom
from org.ict_ok.components.room.interfaces import IRoomFolder
from zope.app.generations.utility import findObjectsProviding
from zope.copypastemove import ObjectMover
from zope.proxy import removeAllProxies
import pprint

roomFolders = [folder for folder in root.values() if IRoomFolder.providedBy(folder)]
roomFolder = roomFolders[0]
buildingFolders = [folder for folder in root.values() if IBuildingFolder.providedBy(folder)]
buildingFolder = buildingFolders[0]
locationFolders = [folder for folder in root.values() if ILocationFolder.providedBy(folder)]
locationFolder = locationFolders[0]


#pprint.pprint([ikroom.ikName for ikroom in findObjectsProviding(root, IRoom)])
#pprint.pprint([ikroom.__parent__.ikName for ikroom in findObjectsProviding(root, IRoom)])
#pprint.pprint([ikroom.building.ikName for ikroom in findObjectsProviding(root, IRoom) if ikroom.building])
rooms2 = [ikroom for ikroom in findObjectsProviding(root, IRoom) if not IRoomFolder.providedBy(ikroom.__parent__)]
for room2 in rooms2: room2.building=room2.__parent__
for room2 in rooms2: ObjectMover(removeAllProxies(room2)).moveTo(roomFolder)
#pprint.pprint([ikroom.building.ikName for ikroom in rooms2 if ikroom.building])


buildings2  = [ikbuilding for ikbuilding in findObjectsProviding(root, IBuilding) if not IBuildingFolder.providedBy(ikbuilding.__parent__)]    
for building2 in buildings2: building2.location=building2.__parent__
for building2 in buildings2: ObjectMover(removeAllProxies(building2)).moveTo(buildingFolder)


locations2  = [iklocation for iklocation in findObjectsProviding(root, ILocation) if not ILocationFolder.providedBy(iklocation.__parent__)]    
for location2 in locations2: ObjectMover(removeAllProxies(location2)).moveTo(locationFolder)


import transaction
transaction.commit()


#zz=removeAllProxies(rooms2[3])
#mover = ObjectMover(zz)


#(Pdb) mover.moveableTo(roomFolder)
#True

#mover.moveTo(roomFolder)




------------------------------------------------

$ bin/zopectl debug

from zope.component import getUtility



from zope.app.generations.utility import findObjectsProviding
from org.ict_ok.components.room.interfaces import IRoom
from org.ict_ok.components.room.interfaces import IRoomFolder


from lovely.relation.app import O2OStringTypeRelationships
from lovely.relation.interfaces import IO2OStringTypeRelationships
rels=getUtility(IO2OStringTypeRelationships)

rels = O2OStringTypeRelationships()
component.provideUtility(rels, IO2OStringTypeRelationships)

from zope.app.intid.interfaces import IIntIds



intIds=getUtility(IIntIds)
component.provideUtility(intIds, IIntIds)


import pprint

pprint.pprint([ikroom.ikName for ikroom in findObjectsProviding(root, IRoom)])

pprint.pprint([ikroom.__parent__.ikName for ikroom in findObjectsProviding(root, IRoom)])

roomFolders = [folder for folder in root.values() if IRoomFolder.providedBy(folder)]
roomFolder = roomFolders[0]


building
for ikroom in findObjectsProviding(root, IRoom):ikroom.building=ikroom.__parent__
