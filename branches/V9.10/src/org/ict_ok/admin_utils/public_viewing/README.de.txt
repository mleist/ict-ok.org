# -*- coding: utf-8 -*-

README zu public_viewing
------------------------

was sind die Klassen, von denen Attribute gezeigt werden sollen?

Das sind alle von Superclass abgeleiteten Inhaltsklassen, die zuvor
von einem berechtigten Admin als Public_viewable markiert wurden.
Von jeder dieser Inhaltsobjekte wird ein Schattenobjekt erzeugt.
Das Schattenobjekt wird in einen Container innerhalb von AdmUtilPublicViewing
abgelegt.
Es wird eine zusätzliche View für das Inhaltsobjekt erzeugt (public.html), die
dann im Submenü des Inhaltsobjektes angezeigt wird (als Menüeintrag) wenn
zuvor für dieses Inhaltsobjekt ein Schattenobjekt erzeugt wurde. In 
PublicDisplay wird zuerst mit getUtility(IAdmUtilPublicViewing) ein
Utilityobjekt geholt und dann aus diesem das zu dem Inhaltsobjekt via
objektId korrespondierende Schattenobjekt geholt. Dieses Schattenobjekt wird
dann im View dargestellt.

Wie erfolgt der Eventaustausch zwischen dem Inhaltsobjekt und dem
korrespondierenden Schattenobjekt?

Wie wird ein Schattenobjekt erzeugt (spezieller Menüeintrag im Submenü des
Inhaltsobjektes)?

[P+]
Es öffnet sich ein Form, in dem können folgende Felder festgelegt werden:
1. Neuer Name (self.ikName)
2. DAU-Description (self.ikComment)
3. aktualisierbare Kopie des Inhalteobjektes.State
   (es werden über den Adapter IState alle Zustandsdaten des Inhaltsobjektes
   bei jeder Änderung in dieses Schattenobjekt eingefügt)

Es braucht noch eine OverView der Schattenobjekte, evtl. noch verschiedene Dar-
stellungen über deren Zustand (rot, gelb,grün)

Ein Schattenobjekt sollte von dem Admin auch wieder gelöscht werden können:
[P-]

TODO:
-----

- ShadowObject implementieren
- AddShadowObjectForm implementieren
   weitere Infos: ... Menüthema???
- EditShadowObjectForm implementieren
- DetailsShadowObjectForm (für Admin) implementieren
- public.html implementieren (Template) siehe superclass.browser.superclass.Overview
- Event-mechanismus implementieren (durch dem ModifiyEvent wird der Inhalt des
  InhalteObject.State in das ShadowObject.State übertragen.)