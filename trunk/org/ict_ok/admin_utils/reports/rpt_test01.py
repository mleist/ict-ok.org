# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=W0232
#
"""rpt_test01 

fill ict-ok.org reporting with karl may 
"""

__version__ = "$Id$"

# ict-ok.org imports
from org.ict_ok.admin_utils.reports.rpt_document import RptDocument
from org.ict_ok.admin_utils.reports.rpt_chapter import RptChapter
from org.ict_ok.admin_utils.reports.rpt_para import RptPara
from org.ict_ok.admin_utils.reports.rpt_title import RptTitle

class RptTest01:
    """chapter01 of karl may / silbersee 
    """
    def __init__(self, filename="/tmp/rpt001.pdf"):
        """
        constructor of the object
        """
        self._document = RptDocument(filename)
        self._document.setVolumeNo("B")
        self._document.setAuthorName("Karl May")
        self._document.setVersionStr("Vers. 0.0.1 $Rev$")
        
        title = RptTitle(u"Der Schatz im Silbersee",
                         doc=self._document)
        self._document.append(title.genElements())

        title = RptTitle(u"Der schwarze Panther",
                         doc=self._document,
                         intype='Heading2')
        self._document.append(title.genElements())

        chapt_01_list = [
            u'Es war um die Mittagszeit eines sehr heißen Junitags, '
            u'als der "Dogfish", einer der größten Passagier- und '
            u'Güterdampfer des Arkansas, mit seinen mächtigen Schaufelrädern '
            u'die Fluten des Stromes peitschte. Er hatte am frühen Morgen '
            u'Little Rock verlassen und sollte nun bald Lewisburg erreichen, '
            u'um dort anzulegen, falls neue Passagiere oder Güter '
            u'aufzunehmen seien.',

            u'Die große Hitze hatte die besser situierten Reisenden in ihre '
            u'Kajüten und Kabinen getrieben, und die meisten der '
            u'Deckpassagiere lagen hinter Fässern, Kisten und andern '
            u'Gepäckstücken, welche ihnen ein wenig Schatten gewährten. '
            u'Für diese Passagiere hatte der Kapitän unter einer '
            u'ausgespannten Leinwand einen Bed-and-board errichten lassen, '
            u'auf welchem allerlei Gläser und Flaschen standen, deren '
            u'scharfer Inhalt jedenfalls nicht für verwöhnte Gaumen und '
            u'Zungen berechnet war. Hinter diesem Schenktisch saß der '
            u'Kellner mit geschlossenen Augen, von der Hitze ermüdet, mit '
            u'dem Kopfe nickend. Wenn er einmal die Lider hob, wand sich ein '
            u'leiser Fluch oder sonst ein kräftiges Wort über seine Lippen. '
            u'Dieser sein Unmut galt einer Anzahl von wohl zwanzig Männern, '
            u'welche vor dem Tische in einem Kreise auf dem Boden saßen und '
            u'den Würfelbecher von Hand zu Hand gehen ließen. Es wurde um '
            u'den sogenannten "Drink" gespielt, d.h. der Verlierende hatte '
            u'am Schlusse der Partie für jeden Mitspielenden ein Glas '
            u'Schnaps zu bezahlen. Infolgedessen war dem Kellner das '
            u'Schläfchen, zu welchem er so große Lust verspürte, versagt.',

            u'Diese Männer hatten sich jedenfalls nicht erst hier auf dem '
            u'Steamer zusammengefunden, denn sie nannten einander "du" und '
            u'schienen, wie gelegentliche Äußerungen verrieten, ihre '
            u'gegenseitigen Verhältnisse genau zu kennen. Entgegengesetzt '
            u'dieser allgemeinen Vertraulichkeit gab es unter ihnen einen, '
            u'dem eine gewisse Art von Respekt erwiesen wurde. Man nannte '
            u'ihn Cornel, eine gebräuchliche Verstümmelung des Wortes '
            u'Colonel, Oberst.',

            u'Dieser Mann war lang und hager; sein glatt rasiertes, scharf '
            u'und spitz gezeichnetes Gesicht wurde von einem borstigen roten '
            u'Kehlbarte umrahmt; fuchsrot waren auch die kurzgeschorenen '
            u'Kopfhaare, wie man sehen konnte, da er den alten, '
            u'abgegriffenen Filzhut weit in den Nacken geschoben hatte. Sein '
            u'Anzug bestand aus schweren, nägelbeschlagenen Lederschuhen, '
            u'Nankingbeinkleidern und einem kurzen Jackett von demselben '
            u'Stoffe. Eine Weste trug er nicht; an Stelle derselben war ein '
            u'ungeplättetes, schmutziges Hemd zu sehen, dessen breiter '
            u'Kragen, ohne von einem Halstuche gehalten zu werden, weit '
            u'offen stand und die nackte, sonnenverbrannte Brust sehen ließ. '
            u'Um die Hüften hatte er sich ein rotes Fransentuch geschlungen, '
            u'aus welchem die Griffe des Messers und zweier Pistolen '
            u'blickten. Hinter ihm lag ein ziemlich neues Gewehr und ein '
            u'leinener Schnappsack, welcher mit zwei Bändern versehen war, '
            u'um auf dem Rücken getragen zu werden.',

            u'Die andern Männer waren in ähnlicher Weise sorglos und gleich '
            u'schmutzig gekleidet, dafür aber sehr gut bewaffnet. Es befand '
            u'sich kein einziger unter ihnen, dem man beim ersten Blicke '
            u'hätte Vertrauen schenken können. Sie trieben ihr Würfelspiel '
            u'mit wahrer Leidenschaftlichkeit und unterhielten sich dabei in '
            u'so rohen Ausdrücken, daß ein halbwegs anständiger Mensch '
            u'sicher keine Minute lang bei ihnen stehen geblieben wäre. '
            u'Jedenfalls hatten sie schon manchen "Drink" gethan, denn ihre '
            u'Gesichter waren nicht nur von der Sonne erhitzt, sondern der '
            u'Geist des Branntweins führte bereits die Herrschaft über sie.',
        ]

        for para_text in chapt_01_list:
            para = RptPara(para_text,
                           doc=self._document)
            self._document.append(para)
        
        title = RptTitle(u"Die Tramps",
                         doc=self._document,
                         intype='Heading2')
        self._document.append(title.genElements())
        chapt_02_list = [
            u'"Die Vereinigten Staaten von Nordamerika sind trotz oder '
            u'vielmehr infolge ihrer freisinnigen Institutionen der Herd '
            u'ganz eigenartiger sozialer Landplagen, welche in einem '
            u'europäischen Staate vollständig unmöglich sein würden."',

            u'Der Kenner der dortigen Zustände wird zugeben, daß diese '
            u'Behauptung eines neueren Geographen ihre guten Gründe habe. '
            u'Man könnte die Plagen, von denen er spricht, in chronische und '
            u'akute einteilen. In ersterer Beziehung wären vor allen Dingen '
            u'die händelsuchenden Loafers und Rowdies, und sodann die '
            u'sogenannten Runners, welche es vorzugsweise auf die '
            u'Einwanderer abgesehen haben, zu nennen. Das Runner-, Loafer- '
            u'und Rowdytum ist stabil geworden und wird, wie es allen '
            u'Anschein hat, noch verschiedene Jahrzehnte überdauern.',
            
            u'Anders ist es bei der zweiten Art der Plagen, welche sich '
            u'schneller entwickeln und von kürzerer Dauer sind. Dahin '
            u'gehörten die rechtlosen Zustände des fernen Westens, infolge '
            u'deren sich förmliche Räuber- und Mörderbanden bildeten, welche '
            u'Master Lynch nur durch das energischeste Vorgehen zu '
            u'vernichten vermochte. Ferner wären hier die Kukluxes zu '
            u'erwähnen, welche während des Bürgerkrieges und auch noch nach '
            u'demselben ihr Wesen trieben. Zur schlimmsten und '
            u'gefährlichsten Landplage aber entwickelten sich die Tramps als '
            u'Vertreter des rohesten und brutalsten Vagabundentums.',

            u'Als zu einer gewissen Zeit ein schwerer Druck auf Handel und '
            u'Wandel lag, Tausende von Fabriken stillstanden und '
            u'Zehntausende von Arbeitern beschäftigungslos wurden, begaben '
            u'sich die Arbeitslosen auf die Wanderung, welche vorzugsweise '
            u'in westlicher Richtung erfolgte. Die am und jenseits des '
            u'Mississippi liegenden Staaten wurden von ihnen förmlich '
            u'überschwemmt. Dort trat bald ein Scheideprozeß ein, indem die '
            u'Ehrlichen unter ihnen Arbeit nahmen, wo sie dieselbe fanden, '
            u'selbst wenn die Beschäftigung nur eine wenig lohnende und '
            u'dabei anstrengende war. Sie traten meist auf Farmen an, um bei '
            u'der Ernte zu helfen, und wurden deshalb gewöhnlich Harvesters, '
            u'Erntearbeiter genannt.',

            u'Die arbeitsscheuen Elemente aber vereinigten sich zu Banden, '
            u'welche von Raub, Mord und Brand ihr Leben fristeten. Die '
            u'Mitglieder derselben sanken schnell auf die tiefste Stufe '
            u'sittlicher Verkommenheit herab und wurden von Männern '
            u'angeführt, welche die Zivilisation meiden mußten, weil die '
            u'Faust des Strafgesetzes sich verlangend nach ihnen '
            u'ausstreckte.',

            u'Diese Tramps (Vagabunden) erschienen gewöhnlich in größeren '
            u'Haufen, zuweilen bis dreihundert Köpfe stark und darüber. '
            u'Sie überfielen nicht bloß einzelne Farmen, sondern selbst '
            u'kleinere Städte, um sie vollständig auszurauben. Sie '
            u'bemächtigten sich sogar der Eisenbahnen, überwältigten die '
            u'Beamten und bedienten sich der Züge, um schnell in ein andres '
            u'Gebiet zu gelangen und dort dieselben Verbrechen zu '
            u'wiederholen. Dieses Unwesen nahm so überhand, daß in einigen '
            u'Staaten die Gouverneurs gezwungen waren, die Miliz '
            u'einzuberufen, um den Strolchen förmliche Schlachten zu '
            u'liefern.',

            u'Für solche Tramps hatten der Kapitän und der Steuermann des '
            u'"Dogfish", wie bereits erwähnt, den Cornel Brinkley und seine '
            u'Leute gehalten. Diese Vermutung konnte, selbst wenn sie '
            u'richtig war, keinen Grund zu direkten Befürchtungen bieten. '
            u'Die Gesellschaft war nur ungefähr zwanzig Mann stark und also '
            u'viel zu schwach, um mit den[28]übrigen Passagieren und der '
            u'Schiffsbesatzung anzubinden, doch konnten Vorsicht und '
            u'Aufmerksamkeit keineswegs als überflüssig gelten.',

            u'Der Cornel hatte seine Aufmerksamkeit natürlich auch auf die '
            u'wunderliche Gestalt gerichtet, welche sich dem Schiffe auf so '
            u'zerbrechlichem Flosse näherte und, nur so wie beiläufig, das '
            u'mächtige Raubtier erlegte. Er hatte gelacht, als Tom den '
            u'sonderbaren Namen Tante Droll aussprach. Aber jetzt, als der '
            u'Fremde das Verdeck betrat und er das Gesicht desselben '
            u'deutlicher erkennen konnte, zogen sich seine Brauen zusammen, '
            u'und er wies seine Leute an, mit ihm zu kommen. Er führte sie '
            u'nach der Spitze des Vorderdecks und antwortete, als man ihn '
            u'nach dem Grunde dieses Rückzuges fragte: "Dieser Kerl ist gar '
            u'nicht so lächerlich, wie er erscheinen will; ich sage euch '
            u'sogar, daß wir uns vor ihm in acht zu nehmen haben."',
        ]
        for para_text in chapt_02_list:
            para = RptPara(para_text,
                           doc=self._document,
                           encoding='utf8')
            self._document.append(para)

        title = RptTitle(u"Nächtliche Kämpfe",
                         doc=self._document,
                         intype='Heading2')
        self._document.append(title.genElements())
        chapt_03_list = [
            u'Am hohen Ufer des Black-bear-Flusses brannte ein großes Feuer. '
            u'Zwar stand der Mond am Himmel, aber sein Licht vermochte '
            u'nicht, die dichten Wipfel der Bäume zu durchdringen, unter '
            u'denen ohne das Feuer tiefe Finsternis geherrscht hätte. Die '
            u'Flamme desselben beleuchtete eine Art Blockhaus, welches nicht '
            u'aus horizontal übereinander lagernden Stämmen, sondern in '
            u'andrer Weise errichtet war. Man hatte von vier in den Winkeln '
            u'eines regelmäßigen Vierecks stehenden Bäumen die Wipfel '
            u'abgesägt und auf die Stämme Querhölzer gelegt, welche das Dach '
            u'trugen. Dieses letztere bestand aus sogenannten Clap-boards, '
            u'Brettern, welche man roh aus astlosen Cypressen- oder auch '
            u'Roteichenstämmen spaltet. In der vordern Wand waren drei '
            u'Öffnungen gelassen, eine größere als Thür und zwei kleinere, '
            u'zu den Seiten der vorigen, als Fenster. Vor diesem Hause '
            u'brannte das erwähnte Feuer und um dasselbe saßen gegen zwanzig '
            u'wilde Gestalten, denen es anzusehen war, daß sie längere Zeit '
            u'nicht mit der sogenannten Zivilisation in Berührung gekommen '
            u'waren. Ihre Anzüge waren abgerissen und ihre Gesichter von '
            u'Sonne, Wind und Wetter nicht nur gebräunt, sondern förmlich '
            u'gegerbt. Außer den Messern hatten sie keine Waffen bei sich; '
            u'diese mochten vielmehr im Innern des Blockhauses liegen.',

            u'Über dem Feuer hing von einem starken Baumaste herab ein '
            u'großer, eiserner Kessel, in welchem mächtige Stücke Fleisches '
            u'kochten. Neben dem Feuer standen zwei ausgehöhlte '
            u'Riesenkürbisse mit gegorenem Honigwasser, also Met. Wer Lust '
            u'dazu hatte, schöpfte sich[60]einen solchen Trunk oder nahm '
            u'sich einen Becher voll Fleischbrühe aus dem Kessel.',

            u'Dabei wurde eine lebhafte Unterhaltung geführt. Die '
            u'Gesellschaft schien sich sehr sicher zu fühlen, denn keiner '
            u'gab sich die Mühe, leise zu sprechen. Hätten diese Leute die '
            u'Nähe eines Feindes angenommen, so wäre das Feuer wohl nach '
            u'indianischer Weise genährt worden, so daß es eine nur kleine, '
            u'nicht weit sichtbare Flamme gab. An der Wand des Hauses '
            u'lehnten Äxte, Beile, große Sägen und andres Handwerkszeug, aus '
            u'welchem sich erraten ließ, daß man eine Gesellschaft von '
            u'Rafters, also von Holzhauern und Flößern, vor sich habe.',

            u'Diese Rafters sind eine ganz eigene Art der Hinterwäldler. '
            u'Sie stehen zwischen den Farmern und Fallenstellern mitten '
            u'inne. Während der Farmer zur Zivilisation in näherer Beziehung '
            u'steht und zu den seßhaften Leuten gehört, führt der Trapper, '
            u'der Fallensteller ein beinahe wildes Leben, ganz ähnlich dem '
            u'Indianer. Auch der Rafter ist nicht an die Scholle gebunden '
            u'und führt ein freies, fast unabhängiges Dasein. Er streift aus '
            u'einem Staate in den andern und aus einer County in die andre. '
            u'Menschen und deren Wohnungen sucht er nicht gern auf, weil das '
            u'Gewerbe, welches er treibt, eigentlich ein ungesetzliches ist. '
            u'Das Land, auf welchem er Holz schlägt, ist nicht sein '
            u'Eigentum. Es fällt ihm auch nur selten ein, zu fragen, wem es '
            u'gehört. Findet er passende Waldung und ein zum Verflößen '
            u'bequemes Wasser in der Nähe, so beginnt er seine Arbeit, ohne '
            u'sich darum zu bekümmern, ob der Ort, wo er sich befindet, '
            u'Kongreßland ist oder schon einem Privateigentümer gehört. Er '
            u'fällt, schneidet und bearbeitet die Stämme, sucht sich dazu '
            u'nur die besten Bäume aus, verbindet sie zu Flößen und schwimmt '
            u'auf denselben dann abwärts, um das erbeutete Gut irgendwo zu '
            u'verkaufen.',

            u'Der Rafter ist ein nicht gern gesehener Gast. Zwar ist es '
            u'wahr, daß manchem neuen Ansiedler der dichte Wald, den er '
            u'vorfindet, zu schaffen macht, und daß er froh wäre, denselben '
            u'gelichtet vorzufinden, aber der Rafter lichtet nicht. Er '
            u'nimmt, wie gesagt, nur die besten Stämme, schneidet die Kronen '
            u'ab und läßt sie liegen. Unter und zwischen diesen Wipfeln '
            u'sprossen dann neue Schößlinge hervor, welche durch wilde Reben '
            u'und andre Schlingpflanzen zu einem festen Ganzen verbunden '
            u'werden, gegen welches die Axt und oft sogar auch das Feuer nur '
            u'wenig vermag.',

            u'Dennoch bleibt der Rafter meist unbelästigt, denn er ist ein '
            u'kräftiger und kühner Gesell, mit welchem in der Wildnis, fern '
            u'von aller Hilfe, nicht so leicht jemand anzubinden wagt. '
            u'Allein kann er natürlich[61]nicht arbeiten, sondern es thun '
            u'sich stets mehrere, meist vier bis acht oder zehn zusammen. '
            u'Zuweilen kommt es auch vor, daß die Gesellschaft aus noch mehr '
            u'Personen besteht; dann fühlt sich der Rafter doppelt sicher, '
            u'denn mit einer solchen Anzahl von Menschen, welche um den '
            u'Besitz eines Baumstammes ihr Leben auf das Spiel setzen '
            u'würden, wird kein Farmer oder sonstiger Besitzer einen Streit '
            u'beginnen.',

            u'Freilich führen sie ein sehr hartes, anstrengungs- und '
            u'entbehrungsreiches Leben, doch ist am Ende ihr Lohn kein '
            u'geringer. Der Rafter verdient, da ihn das Material nichts '
            u'kostet, ein schönes Stück Geld. Während die andern arbeiten, '
            u'sorgt ein Kamerad oder sorgen zwei oder mehrere, je nach der '
            u'Größe der Gesellschaft, für die Ernährung derselben. Das sind '
            u'die Jäger, welche tagsüber und oft auch während der Nacht '
            u'umherstreifen, um "Fleisch zu machen". In wildreichen Gegenden '
            u'ist das nicht schwer. Mangelt es aber an Wild, so gibt es viel '
            u'zu thun; der Jäger hat keine Zeit übrig, Honig und andre '
            u'Delikatessen zu suchen, und die Rafters müssen auch diejenigen '
            u'Fleischstücke essen, welche der Hinterwäldler sonst '
            u'verschmäht, sogar die Eingeweide.',

            u'Die Gesellschaft nun, welche hier am schwarzen Bärenflusse ihr '
            u'Wesen trieb, schien, wie der volle Kessel bewies, keine Not zu '
            u'leiden. Darum waren alle guter Laune, und es wurde nach der '
            u'harten Tagesarbeit viel gescherzt. Man erzählte sich heitre '
            u'oder sonst interessante Erlebnisse; man schilderte Personen, '
            u'welche man getroffen hatte und die irgend eine Eigenschaft '
            u'besaßen, welche zum Lachen Veranlassung gab.',

            u'"Da solltet ihr einen kennen, den ich da oben mal in Fort '
            u'Niobrara getroffen habe," sagte ein alter, graubärtiger Kerl. '
            u'"Der Mann war ein Mann und wurde doch nur Tante genannt."',

            u'"Meinst du etwa Tante Droll?" fragte ein andrer.',

            u'"Ja, grad den und keinen andern meine ich. Bist du ihm etwa '
            u'auch begegnet?"',

            u'"Ja, einmal. Das war in Desmoines, im Gasthofe, wo sein '
            u'Erscheinen große Aufmerksamkeit erregte und sich alle über '
            u'ihn lustig machten. Besonders einer war es, der ihm keine Ruhe '
            u'ließ, bis Droll ihn bei den Hüften nahm und zum Fenster '
            u'hinauswarf. Der Mann kam nicht wieder herein."',

            u'"Das traue ich der Tante gut und gern zu. Droll liebt einen '
            u'Spaß und hat nichts dagegen, wenn man über ihn lacht, aber '
            u'über einen gewissen Punkt hinaus darf man nicht gehen, sonst '
            u'zeigt er die Zähne. Übrigens würde ich einen jeden, der ihn '
            u'ernstlich beleidigen wollte, sofort niederschlagen."',

            u'"Du, Blenter? Warum?"',

            u'"Darum, weil ich ihm mein Leben verdanke. Ich bin mit ihm bei '
            u'den Sioux gefangen gewesen. Ich sage euch, daß ich damals '
            u'gewiß und wirklich von ihnen in die ewigen Jagdgründe '
            u'geschickt worden wäre. Ich bin nicht der Mann, der sich vor '
            u'drei oder fünf Indianern fürchtet; ich pflege auch nicht zu '
            u'wimmern, wenn es mir einmal verkehrt geht; damals aber war '
            u'keine Spur von Hoffnung mehr vorhanden, und ich wußte '
            u'wahrhaftig keinen Ausweg. Dieser Droll aber ist ein Pfiffikus '
            u'sondergleichen; er hat die Roten so eingeseift, daß sie nicht '
            u'mehr aus den Augen sehen konnten. Wir entkamen."',

            u'"Wie war das? Wie ging das zu? Erzähle, erzähle!"',

            u'"Wenn es dir recht ist, werde ich lieber den Mund halten. Es '
            u'ist kein Vergnügen, eine Begebenheit zu berichten, bei welcher '
            u'man keine rühmliche Rolle gespielt hat, sondern von den Roten '
            u'übertölpelt wurde. Genug, daß ich dir sage, wenn ich heut hier '
            u'sitze und mir den Rehbock schmecken lassen kann, so habe ich '
            u'das nicht mir, sondern der Tante Droll zu danken."',

            u'"So muß die Tinte, in welcher du saßest, sehr tief und schwarz '
            u'gewesen sein. Der alte Missouri-Blenter ist doch als ein '
            u'Westmann bekannt, welcher gewiß die Thür findet, wenn '
            u'überhaupt eine vorhanden ist."',

            u'"Damals aber habe ich sie nicht gefunden. Ich stand fast '
            u'schon unter dem Marterpfahle."',

            u'"Wahrhaftig? Das ist freilich eine Situation, in welcher es '
            u'wenig Aussicht auf Entkommen gibt. Eine verteufelte Erfindung, '
            u'dieser Marterpfahl! Ich hasse die Canaillen doppelt, wenn '
            u'ich an dieses Wort denke."',

            u'"So weißt du nicht, was du thust und was du sagst. Wer die '
            u'Indsmen haßt, der beurteilt sie falsch, der hat nicht darüber '
            u'nachgedacht, was die Roten alles erduldet haben. Wenn jetzt '
            u'jemand käme, um uns von hier zu vertreiben, was '
            u'würdest du thun?"',

            u'"Mich wehren, und sollte es sein oder mein Leben kosten."',
        ]
        for para_text in chapt_03_list:
            para = RptPara(para_text,
                           doc=self._document,
                           encoding='utf8')
            self._document.append(para)

    def outConsole(self):
        """
        output per print
        """
        self._document.outConsole()
        
    def outPdf(self):
        """
        putput per pdf
        """
        self._document.buildPdf()

    def outConsoleTree(self):
        """
        output per print
        """
        self._document.outConsoleTree()

if __name__== '__main__':
    rpt_t01 = RptTest01()
    print "------------------------------------"
    #rpt_t01.outConsole()
    rpt_t01.outPdf()
    print "------------------------------------"
    #rpt_t01.outConsoleTree()
