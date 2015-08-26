# -*- coding: UTF-8 -*-

#
#   Eine Pythonimplementation des Porter-Stemmers für Deutsch (Orginal unter http://snowball.tartarus.org/texts/germanic.html)
#
#   Ersteller dieser Version: (c) by kristall 'ät' c-base.org       http://kristall.crew.c-base.org/protected/porter_stemmer/porter_de.py
#
#   Der Algorithmus in (englischem) Prosa unter http://snowball.tartarus.org/algorithms/german/stemmer.html
#
#   Wikipedia zum Porter-Stemmer: http://de.wikipedia.org/wiki/Porter-Stemmer-Algorithmus
#
#   Lizenz: Diese Software steht unter der BSD License (siehe http://www.opensource.org/licenses/bsd-license.html).
#   Ursprünglicher Autor: (c) by Dr. Martin Porter
#
#   Bitte UTF-8 benutzen | Please use UTF-8
#

SPECIAL_CHARS = u".:;,?!§$%&/()="


class PorterStemmerGerman:
    """
    Die Funktion stem nimmt ein Wort und versucht dies durch Regelanwendung zu verkürzen. Wenn Stop auf 'True' gesetzt wird, werden Wörter in der Stopliste nicht 'gestemmt'.
    """

    def __init__(self):
        pass

    def stem(self, wort, stop=False):

        # rupert 17072008 if there is any .:? etc in it, do not any stemming!
        for ch in SPECIAL_CHARS:
            if ch in wort:
                return wort

        # ACHTUNG: für den Stemmer gilt 'y' als Vokal.
        vokale = u'aeiouyäüö'
        #   ACHTUNG: 'U' und 'Y' gelten als Konsonaten.
        konsonanten = u'bcdfghjklmnpqrstvwxzßUY'
        #   Konsonanten die vor einer 's'-Endung stehen dürfen.
        s_endung = u'bdfghklmnrt'
        #   Konsonanten die vor einer 'st'-Endung stehen dürfen.
        st_endung = u'bdfghklmnt'
        #   Zu r1 & r2 siehe http://snowball.tartarus.org/texts/r1r2.html, p1 & p2 sind die Start'p'ositionen von r1 & r2 im String
        r1 = ''
        p1 = 0
        r2 = ''
        p2 = 0
        #   Die Stopliste; Wörter in dieser Liste werden nicht 'gestemmt', wenn stop  = 'True' an die Funktion
        #   übergeben wurde
        stopliste = [u'aber', u'alle', u'allem', u'allen', u'aller', u'alles', u'als', u'also', u'am', u'an', u'ander',
                     u'andere', u'anderem',
                     u'anderen', u'anderer', u'anderes', u'anderm', u'andern', u'anders', u'auch', u'auf', u'aus',
                     u'bei', u'bin', u'bis', u'bist',
                     u'da', u'damit', u'dann', u'der', u'den', u'des', u'dem', u'die', u'das', u'dass', u'daß',
                     u'derselbe', u'derselben', u'denselben',
                     u'desselben', u'demselben', u'dieselbe', u'dieselben', u'dasselbe', u'dazu', u'dein', u'deine',
                     u'deinem', u'deinen', u'deiner',
                     u'deines', u'denn', u'derer', u'dessen', u'dich', u'dir', u'du', u'dies', u'diese', u'diesem',
                     u'diesen', u'dieser', u'dieses',
                     u'doch', u'dort', u'durch', u'ein', u'eine', u'einem', u'einen', u'einer', u'eines', u'einig',
                     u'einige', u'einigem', u'einigen',
                     u'einiger', u'einiges', u'einmal', u'er', u'ihn', u'ihm', u'es', u'etwas', u'euer', u'eure',
                     u'eurem', u'euren', u'eurer', u'eures',
                     u'für', u'gegen', u'gewesen', u'hab', u'habe', u'haben', u'hat', u'hatte', u'hatten', u'hier',
                     u'hin', u'hinter', u'ich', u'mich',
                     u'mir', u'ihr', u'ihre', u'ihrem', u'ihren', u'ihrer', u'ihres', u'euch', u'im', u'in', u'indem',
                     u'ins', u'ist', u'jede', u'jedem',
                     u'jeden', u'jeder', u'jedes', u'jene', u'jenem', u'jenen', u'jener', u'jenes', u'jetzt', u'kann',
                     u'kein', u'keine', u'keinem',
                     u'keinen', u'keiner', u'keines', u'können', u'könnte', u'machen', u'man', u'manche', u'manchem',
                     u'manchen', u'mancher',
                     u'manches', u'mein', u'meine', u'meinem', u'meinen', u'meiner', u'meines', u'mit', u'muss',
                     u'musste', u'muß', u'mußte', u'nach',
                     u'nicht', u'nichts', u'noch', u'nun', u'nur', u'ob', u'oder', u'ohne', u'sehr', u'sein', u'seine',
                     u'seinem', u'seinen', u'seiner',
                     u'seines', u'selbst', u'sich', u'sie', u'ihnen', u'sind', u'so', u'solche', u'solchem', u'solchen',
                     u'solcher', u'solches', u'soll',
                     u'sollte', u'sondern', u'sonst', u'über', u'um', u'und', u'uns', u'unse', u'unsem', u'unsen',
                     u'unser', u'unses', u'unter', u'viel',
                     u'vom', u'von', u'vor', u'während', u'war', u'waren', u'warst', u'was', u'weg', u'weil', u'weiter',
                     u'welche', u'welchem',
                     u'welchen', u'welcher', u'welches', u'wenn', u'werde', u'werden', u'wie', u'wieder', u'will',
                     u'wir', u'wird', u'wirst', u'wo',
                     u'wollem', u'wollte', u'würde', u'würden', u'zu', u'zum', u'zur', u'zwar', u'zwischen']
        #   Wortstämme werden klein geschrieben
        wort = wort.lower()
        #   Wenn 'stop' und Wort in Stopliste gib 'wort' zurück
        if stop is True and wort in stopliste:
            return wort
        # Ersetze alle 'ß' durch 'ss'
        while u'ß' in wort:
            wort = wort[:(wort.find(u'ß'))] + u'ss' + wort[((wort.find(u'ß')) + 1):]
        # Schützenswerte u'u' bzw. u'y' werden durch u'U' bzw. u'Y' ersetzt
        for e in map(None, wort, range(len(wort))):
            if e[1] == 0:
                continue
            if u'u' in e:
                try:
                    if (wort[(e[1] - 1)] in vokale) and (wort[(e[1] + 1)] in vokale): wort = wort[:e[1]] + u'U' + wort[(
                        e[1] + 1):]
                except Exception:
                    pass
            if u'y' in e:
                try:
                    if (wort[(e[1] - 1)] in vokale) and (wort[(e[1] + 1)] in vokale): wort = wort[:e[1]] + u'Y' + wort[(
                        e[1] + 1):]
                except Exception:
                    pass
        # r1, r2, p1 & p2 werden mit Werten belegt
        try:
            Bedingung = False
            for e in map(None, wort, range(len(wort))):
                if e[0] in vokale: Bedingung = True
                if (e[0] in konsonanten) and Bedingung:
                    p1 = e[1] + 1
                    r1 = wort[p1:]
                    break
            Bedingung = False
            for e in map(None, r1, range(len(r1))):
                if e[0] in vokale: Bedingung = True
                if (e[0] in konsonanten) and Bedingung:
                    p2 = e[1] + 1
                    r2 = r1[p2:]
                    break
            if (p1 < 3) and (p1 > 0):
                p1 = 3
                r1 = wort[p1:]
            if p1 == 0:
                return self.end_stemming(wort)
        except Exception:
            pass
        # Die Schritte 1 bis 3 d) u'stemmen' das übergebene Wort.
        #   Schritt 1
        eSuffixe_1 = [u'e', u'em', u'en', u'ern', u'er', u'es']
        eSonst_1 = [u's']
        try:
            for e in eSuffixe_1:
                if e in r1[-(len(e)):]:
                    wort = wort[:-(len(e))]
                    r1 = r1[:-(len(e))]
                    r2 = r2[:-(len(e))]
                    break
            else:
                if r1[-1] in eSonst_1:
                    if wort[-2] in s_endung:
                        wort = wort[:-1]
                        r1 = r1[:-1]
                        r2 = r2[:-1]
        except Exception:
            pass
        # Schritt 2
        eSuffixe_2 = [u'est', u'er', u'en']
        eSonst_2 = [u'st']
        try:
            for e in eSuffixe_2:
                if e in r1[-len(e):]:
                    wort = wort[:-len(e)]
                    r1 = r1[:-len(e)]
                    r2 = r2[:-len(e)]
                    break
            else:
                if r1[-2:] in eSonst_2:
                    if wort[-3] in st_endung:
                        if len(wort) > 5:
                            wort = wort[:-2]
                            r1 = r1[:-2]
                            r2 = r2[:-2]
        except Exception:
            pass
        # Schritt 3 a)
        dSuffixe_1 = [u'end', u'ung']
        try:
            for e in dSuffixe_1:
                if e in r2[-(len(e)):]:
                    if u'ig' in r2[-(len(e) + 2):-(len(e))]:
                        if u'e' in wort[-(len(e) + 3)]:
                            wort = wort[:-(len(e))]
                            r1 = r1[:-(len(e))]
                            r2 = r2[:-(len(e))]
                            break
                        else:
                            wort = wort[:-(len(e) + 2)]
                            r2 = r2[:-(len(e) + 2)]
                            r1 = r1[:-(len(e) + 2)]
                            break
                    else:
                        wort = wort[:-(len(e))]
                        r2 = r2[:-(len(e))]
                        r1 = r1[:-(len(e))]
                    return self.end_stemming(wort)
        except Exception:
            pass
        # Schritt 3 b)
        dSuffixe_2 = [u'ig', u'ik', u'isch']
        try:
            for e in dSuffixe_2:
                if e in r2[-(len(e)):]:
                    if u'e' in wort[-(len(e) + 1)]:
                        pass
                    else:
                        wort = wort[:-(len(e))]
                        r2 = r2[:-(len(e))]
                        r1 = r1[:-(len(e))]
                        break
        except Exception:
            pass
        # Schritt 3 c)
        dSuffixe_3 = [u'lich', u'heit']
        sonder_1 = [u'er', u'en']
        try:
            for e in dSuffixe_3:
                if e in r2[-(len(e)):]:
                    for i in sonder_1:
                        if i in r1[-(len(e) + len(i)):-(len(e))]:
                            wort = wort[:-(len(e) + len(i))]
                            r1 = r1[:-(len(e) + len(i))]
                            r2 = r2[:-(len(e) + len(i))]
                            break
                    else:
                        wort = wort[:-(len(e))]
                        r1 = r1[:-(len(e))]
                        r2 = r2[:-(len(e))]
                        break

        except Exception:
            pass
        # Schritt 3 d)
        dSuffixe_4 = [u'keit']
        sonder_2 = [u'lich', u'ig']
        try:
            for e in dSuffixe_4:
                if e in r2[-(len(e)):]:
                    for i in sonder_2:
                        if i in r2[-(len(e) + len(i)):-(len(e))]:
                            wort = wort[:-(len(e) + len(i))]
                            break
                    else:
                        wort = wort[:-(len(e))]

        except Exception:
            pass
        return self.end_stemming(wort)

    #   end_stemming verwandelt u'ä', u'ö', u'ü' in den "Grundvokal" und macht u'U' bzw. u'Y' klein.
    def end_stemming(self, wort):
        # rupert 17072008 changed. We return version with and without ü ä etc.
        wort1 = wort
        while u'ä' in wort1:
            wort1 = wort1[:(wort1.find(u'ä'))] + u'a' + wort1[((wort1.find(u'ä')) + 1):]
        while u'ö' in wort1:
            wort1 = wort1[:(wort1.find(u'ö'))] + u'o' + wort1[((wort1.find(u'ö')) + 1):]
        while u'ü' in wort1:
            wort1 = wort1[:(wort1.find(u'ü'))] + u'u' + wort1[((wort1.find(u'ü')) + 1):]
        while u'U' in wort1:
            wort1 = wort1[:(wort1.find(u'U'))] + u'u' + wort1[((wort1.find(u'U')) + 1):]
        while u'Y' in wort1:
            wort1 = wort1[:(wort1.find(u'Y'))] + u'y' + wort1[((wort1.find(u'Y')) + 1):]

        return [wort, wort1]
