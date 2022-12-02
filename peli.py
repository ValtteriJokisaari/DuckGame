import math
import haravasto
import laatikot


IKKUNAN_LEVEYS = 1200
IKKUNAN_KORKEUS = 600
PUTOAMISKIIHTYVYYS = 1.5

peli = {
    "x": 100,
    "y": 100,
    "ritsax": 110,
    "ritsay": 110,
    "kulma": 0,
    "voima": 0,
    "x_nopeus": 0,
    "y_nopeus": 0,
    "lennossa": False,
    "maassa": [],
    "sorsat" : 3,
    "laatikot": [],
    "matolista" : [],
    "taso": 1,
    "random": False,
    "voitto" : 0,
    "raahaus": False,
    "pisteet": [],
    "menu": True,
    "kentät": 3
}

hiiripos = {
    "x": 0,
    "y": 0,
    "nappi": None
}

def alkutila(kutsu=0):
    """
    Asettaa kentän takaisin alkutilaan,
    eli sorsat lähtöpaikkaan, sen nopeudet nollaan, sekä lentotilan epätodeksi.
    """
    peli["x"] = 100
    peli["y"] = 100
    peli["kulma"] = 0
    peli["voima"] = 0
    peli["x_nopeus"] = 0
    peli["y_nopeus"] = 0
    peli["lennossa"] = False
    peli["maassa"] = []
    peli["voitto"] = 0


    if not peli["random"]:
        if peli["taso"] == 1:
            peli["laatikot"], peli["matolista"], peli["sorsat"] = lataa_kartta(1)
        elif peli["taso"] == 2:
            peli["laatikot"], peli["matolista"], peli["sorsat"] = lataa_kartta(2)
        else:
            peli["laatikot"], peli["matolista"], peli["sorsat"] = lataa_kartta(3)
def alusta_peli(kutsu=0):
    """
    Asettaa pelin takaisin alkutilaan,
    eli sorsan lähtöpaikkaan, sen nopeudet nollaan, sekä lentotilan epätodeksi.
    """
    peli["kentät"] = 3
    peli["menu"] = False
    peli["random"] = False
    peli["laatikot"], peli["matolista"], peli["sorsat"] = lataa_kartta(1)
    peli["voitto"] = 0
    peli["x"] = 100
    peli["y"] = 100
    peli["kulma"] = 0
    peli["voima"] = 0
    peli["x_nopeus"] = 0
    peli["y_nopeus"] = 0
    peli["lennossa"] = False
    peli["maassa"] = []
    peli["taso"] = 1


def ammu():

    """
    Funktio lähettää sorsan liikkeelle ja laskee sille lähtönopeuden, sijoittaen x- ja
    y-nopeusvektorit globaaliin sanakirjaan.
    """

    peli["x_nopeus"] = peli["voima"] * math.cos(math.radians(peli["kulma"]))
    peli["y_nopeus"] = peli["voima"] * math.sin(math.radians(peli["kulma"]))
    peli["lennossa"] = True

def lento(kulunut_aika):

    """
    Funktio päivittää laatikon muuttuneet x- ja y-koordinaatit,
    kappaleen nopeusvektorien perusteella. Tarkistaa osumat objektien välillä.
    """
    paalla = 0
    #Tarkastetaan osuuko sorsa objektiin, sekä mikäli objektin päällä astetetaan y_nopeus nollaan ja y koordinaatti oikein.
    for objekti in peli["laatikot"]+peli["matolista"]:
        ehto1 = peli["x"]+40+peli["x_nopeus"]<objekti["x"] or peli["x"]+40+peli["x_nopeus"]>objekti["x"]+objekti["w"]
        ehto2 = (peli["y"]+peli["y_nopeus"]>objekti["y"]+objekti["h"] or peli["y"]+peli["y_nopeus"]<objekti["y"])
        if not ehto1 and not ehto2:

            if objekti["tyyppi"] == "mato":
                objekti["kuollut"] = 1
                continue
            peli["x_nopeus"] = 0
            if peli["y"]+peli["y_nopeus"]<= objekti["y"]+objekti["h"] and not peli["x"]+peli["x_nopeus"]<objekti["x"]:
                peli["y"] = objekti["y"]+objekti["h"]
                peli["y_nopeus"] = 0
                paalla = 1
                
            else:
                peli["x"] = objekti["x"]-40
    #Mikäli sorsa on maassa tai laatikon päällä asetetaan lento Falseen ja miinustetaan sorsa
    if peli["y"] + peli["y_nopeus"] <= 0 or (paalla != 0 and peli["y_nopeus"] == 0) :
        peli["lennossa"] = False
        peli["y_nopeus"] = 0
        paalla = 0
        peli["sorsat"] -= 1
        peli["maassa"].append([(peli.copy()["x"]), peli.copy()["y"]])
        peli["x"] = 100
        peli["y"] = 100
    if peli["lennossa"] is True:
        peli["x"] += peli["x_nopeus"]
        peli["y"] += peli["y_nopeus"]
        gforce = 1.5
        peli["y_nopeus"] -= gforce

def tarkistamadot():
    """
    Tarkistaa hengissä olevien matojen lukumäärän ja palauttaa sen
    """
    madot = len(peli["matolista"])
    for mato in peli["matolista"]:
        if mato["kuollut"] != 0:
            madot -= 1
    return madot

def piirra():
    """
    Tämä funktio piirtää taustan, sorsat, pelitila ruudut.
    """

    teksti = haravasto.piirra_tekstia
    lisaa_ruutu = haravasto.lisaa_piirrettava_ruutu
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    lisaa_ruutu("taustakuva", 1, 1)
    haravasto.piirra_ruudut()

    if peli["menu"]:
        teksti("TERVETULOA SORSAPELIINI!", 200, 330,(255, 0, 0, 255),koko=42)
        lisaa_ruutu("menukuva", 400, 350)
        haravasto.piirra_ruudut()
        teksti("PAINA     , aloitaaksesi normaalin pelin.", 200, 270,(0, 0, 0, 255),koko=30)
        teksti("'A'", 340, 270,(255, 0, 255, 255),koko=30)
        teksti("PAINA     , mikäli haluat pelata satunnaisia karttoja", 200, 210,(0, 0, 0, 255),koko=30)
        teksti("'S'", 340, 210,(255, 0, 255, 255),koko=30)
        teksti("PAINA     , lopettaaksesi pelin", 200, 150,(0, 0, 0, 255),koko=30)
        teksti("'Q'", 340, 150,(255, 0, 255, 255),koko=30)
        return

    #Tarkastaa sorsien lkm ja piirtää ne. Häviöruutu tulee, mikäli voitto ei ole tapahtunut eikä sorsia ole.
    if peli["sorsat"] > 0:
        lisaa_ruutu("sorsa", peli["x"], peli["y"])
        for i in range(peli["sorsat"]-1):
            lisaa_ruutu("sorsa", 60-i*40, 20)
    else:
        if not peli["voitto"]:
            teksti("HÄVISIT :(", 380, 360,(255, 0, 0, 255),koko=42)
            teksti("Sorsat loppuivat kesken", 380, 320,(255, 0, 0, 255),koko=30)
            if peli["random"]:
                teksti("PALAA MENUUN PAINAMALLA", 380, 250,(0, 0, 0, 255),koko=20)
                teksti("'M'", 850, 250,(255, 0, 255, 255),koko=25)
                return
            teksti("Paina      aloittaaksesi uudelleen tason", 380, 290,koko=20)
            teksti("'R'", 460, 290,(255, 0, 255, 255),koko=20)
            teksti("Ei muutaku uutta matoa koukkuun!", 380, 270, koko=20)
    if peli["sorsat"] != 0:
        for sorsa in peli["maassa"]:
            lisaa_ruutu("sorsa", sorsa[0], sorsa[1])

    # Ritsan piirto
    lisaa_ruutu("ritsa", peli["ritsax"]-30, peli["ritsay"]-90)
    
    # Lentoradan pisteet
    if len(peli["pisteet"]) != 0:
        for piste in peli["pisteet"]:
            lisaa_ruutu("piste", piste[0], piste[1])

    #Tarkastaa laatikon tyypin ja piirtää sen
    for i in range(len(peli["laatikot"])):
        if peli["laatikot"][i]["tyyppi"] == "aita":
            lisaa_ruutu("aita", peli["laatikot"][i]["x"], peli["laatikot"][i]["y"])
            continue

        lisaa_ruutu("laatikko", peli["laatikot"][i]["x"], peli["laatikot"][i]["y"])

    #Piirtää hengissä olevat ja kuolleet madot
    if len(peli["matolista"]) != 0:
        for mato in peli["matolista"]:
            if mato["kuollut"] != 0:
                lisaa_ruutu("matokuollut", mato["x"], mato["y"])
            else:
                lisaa_ruutu("mato", mato["x"], mato["y"])
    #Piirtää tekstit
    haravasto.piirra_ruudut()
    teksti("{}°\tVoima: {}".format(round(peli["kulma"]), round(peli["voima"])), 10, 505)
    teksti("Sorsat: {}".format(peli["sorsat"]), 10, 250)
    teksti("Matoja jäljellä: {}".format(tarkistamadot()), 550, 505)
    teksti("Taso: {} / {} ".format(peli["taso"],(peli["kentät"])), 550, 550)
    if not peli["random"]:
        teksti(
            "Q: Lopeta  | "
            "R: Reset | "
            "M: Menu | " , 
            10, 560, koko=20
        )
    else:
        teksti(
            "Q: Lopeta  | "
            "M: Menu | " , 
            10, 560, koko=20
        )
    teksti(
        "Hiiri vasen: Säädä kulma ja voima vetämällä ritsaa",
        10, 230, koko=10
    )
    teksti(
        "Päästä irti ja laukaise!",
        10, 210, koko=10
    )
    #Voittomenun piirto
    if peli["voitto"] == 1:
        if peli["taso"] == 3 and not peli["random"]:
            teksti("VOITIT PELIN!!", 300, 330,(50, 255, 50, 255),koko=42)
            teksti("PELAA UUDELLEEN PAINAMALLA", 300, 300,(0, 0, 0, 255),koko=20)
            teksti("'A'", 770, 300,(255, 0, 255, 255),koko=25)
            teksti("PALAA MENUUN PAINAMALLA", 300, 250,(0, 0, 0, 255),koko=20)
            teksti("'M'", 770, 250,(255, 0, 255, 255),koko=25)
        else:
            teksti("VOITIT TASON!", 380, 260,(50, 255, 50, 255),koko=42)
    else:
        if peli["sorsat"] == 0 and not peli["lennossa"]:
            pass

def nappain(sym, mods):
    """
    Tämä funktio hoitaa näppäinsyötteiden käsittelyn.
    Funktiota ei tarvitse muokata.
    """
    key = haravasto.pyglet.window.key

    if sym == key.Q:
        haravasto.lopeta()
    if sym == key.S:
        if not peli["menu"]:
            return
        alusta_peli()
        peli["random"] = True
        peli["kentät"] = "∞"
        peli["laatikot"], peli["matolista"], peli["sorsat"] = laatikot.random_kartta()
    if sym == key.R:
        if not peli["random"]:
            alkutila()
    if sym == key.A:
        if peli["menu"] or (peli["taso"] == 3 and peli["voitto"]):
            alusta_peli()
    if sym == key.M:
        alusta_peli()
        peli["menu"] = True
def kasittele_raahaus(hiirix, hiiriy, xdis, ydis, button, muokkaus):
    """
    Tätä funktiota kutsutaan kun käyttäjä liikuttaa hiirtä jonkin painikkeen
    ollessa painettuna. Siirtää ruudulla olevaa laatikkoa saman verran kuin kursori
    liikkui.

    """
    if peli["lennossa"] or peli["sorsat"]<1:
        return

    if 110>peli["x"]>0 and 220>peli["y"]>20:
        if peli["x"]-40<hiirix<peli["x"]+40 and peli["y"]-40<hiiriy<peli["y"]+40:
            peli["raahaus"] = True
            peli["x"] = hiirix - 20
            peli["y"] = hiiriy - 20
            x_2 = peli["ritsax"]
            y_2 = peli["ritsay"]
            erox = hiirix - x_2 
            if erox == 0:
                erox = 0.00000001
            eroy = hiiriy - y_2
            peli["kulma"] = (math.degrees(math.atan(float(eroy)/float(erox))))
            peli["voima"] = (math.sqrt((erox)**2 + (eroy)**2)) * 0.6
        else:
            peli["voima"] = 0

    else:
        peli["raahaus"] = False
        peli["x"] = 100
        peli["y"] = 100
        peli["kulma"] = 0
        peli["voima"] = 0

        return

def lentorata(kulunut_aika):
    """
    Animoi lentoradan laskemalla pisteitä kulman ja voiman perusteella ja lisää ne pisteet listaan.
    """
    if peli["raahaus"]:
        peli["pisteet"] = []
        lentoratax = peli["x"]
        lentoratay = peli["y"]
        x_nopeus = peli["voima"] * math.cos(math.radians(peli["kulma"]))
        y_nopeus = peli["voima"] * math.sin(math.radians(peli["kulma"]))
        for piste in range(60):
            gforce = 1.5
            lentoratax += x_nopeus
            lentoratay += y_nopeus
            y_nopeus -= gforce
            peli["pisteet"].append([lentoratax, lentoratay])
            if lentoratax > IKKUNAN_LEVEYS or lentoratay <= 0:
                break
    else:
        peli["pisteet"] = []
    



def paivita(kulunut_aika):
    """
    Päivittaaa ohjelman
    """

    if peli["menu"]:
        return
    laatikot.pudota(peli["laatikot"]+peli["matolista"])
    if 80<hiiripos["x"]<120 and 80<hiiripos["y"]<140 and hiiripos["nappi"] == 1:
        haravasto.aseta_raahaus_kasittelija(kasittele_raahaus)

    if tarkistamadot() == 0:
        if peli["voitto"] == 1:
            return
        peli["voitto"] = 1
        haravasto.pyglet.clock.schedule_once(voitto, 2)
    
def voitto(taso):
    """
    Tarkistetaan taso ja asetetaan alkutilaan. Sen jälkeen taso kasvaa yhdellä ja kartta vaihtuu
    """
    taso = peli["taso"]
    if peli["random"]:
        alkutila()
        peli["laatikot"], peli["matolista"], peli["sorsat"] = laatikot.random_kartta()
        peli["taso"] += 1
        return
    if taso == 3:
        return
    alkutila()
    if taso == 1:
        peli["laatikot"], peli["matolista"], peli["sorsat"] = lataa_kartta(2)
        peli["taso"] = 2
    elif taso == 2:
        peli["laatikot"], peli["matolista"], peli["sorsat"] = lataa_kartta(3)
        peli["taso"] = 3


def hiiri_kasittelija(hiirix, hiiriy, nappi, muokkausnapit):
    """
    Ottaa hiiren sijainnin ja napin mitä käytetään.
    """
    hiiripos["x"] = hiirix
    hiiripos["y"] = hiiriy
    hiiripos["nappi"] = nappi

def vapautus_kasittelija(x, y, nappi, muokkausnapit):
    """
    Ampuu sorsan mikäli raahaus vapautetaan.
    """
    if nappi == 1 and peli["raahaus"]:
        ammu()
        peli["raahaus"] = False

def lataa_kartta(numero):
    """
    Lataa kartan laatikot moduulin avulla
    """
    if numero == 1:
        kartta = laatikot.kartta(1)
    elif numero == 2:
        kartta = laatikot.kartta(2)
    else:
        kartta = laatikot.kartta(3)
    return kartta

if __name__ == "__main__":
    haravasto.lataa_kuvat("spritet")
    haravasto.lataa_sorsa("spritet")
    haravasto.luo_ikkuna(leveys=IKKUNAN_LEVEYS, korkeus=IKKUNAN_KORKEUS)
    haravasto.aseta_piirto_kasittelija(piirra)
    haravasto.aseta_nappain_kasittelija(nappain)
    haravasto.aseta_toistuva_kasittelija(lento)
    haravasto.aseta_toistuva_kasittelija(paivita)
    haravasto.aseta_toistuva_kasittelija(lentorata, 1/45)
    haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
    haravasto.aseta_vapautus_kasittelija(vapautus_kasittelija)
    haravasto.aloita()
