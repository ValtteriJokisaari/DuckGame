"""
Käsittelee karttojen lataamisen, satunnaiskentän generaation ja laatikoiden pudottamisen. 
"""
import random
import json
import haravasto

IKKUNAN_LEVEYS = 1200
IKKUNAN_KORKEUS = 600
PUTOAMISKIIHTYVYYS = 1.5

peli = {
    "laatikot": []
}

def luo_laatikot(lkm, raja):
    """
    Luo halutun määrän laatikoita ja asettaa ne satunnaisiin kohtiin määritetyn
    alueen sisälle. Laatikot esitetään sanakirjoilla joissa on seuraavat avaimet:
    x: vasemman alakulman x-koordinaatti
    y: vasemman alakulman y-koordinaatti
    w: laatikon leveys
    h: laatikon korkeus
    vy: laatikon putoamisnopeus
    """
    laatikkolista = []
    laatikko = {
        "x": 0,
        "y": 0,
        "w": 80,
        "h": 80,
        "tyyppi": "laatikko",
        "vy": 0
    }
    matolista = []
    mato = {
        "x": 0,
        "y": 0,
        "w": 80,
        "h": 80,
        "tyyppi": "mato",
        "kuollut": 0,
        "vy": 0
    }

    for i in range(lkm):
        randy = random.randint(raja, IKKUNAN_KORKEUS-raja)
        randx = random.randint(2*raja, IKKUNAN_LEVEYS-raja)
        laatikkolista.append(laatikko.copy())
        laatikkolista[i]["x"] = randx
        laatikkolista[i]["y"] = randy

    for i in range(lkm - 6):
        randx = random.randint(2*raja, IKKUNAN_LEVEYS-raja)
        matolista.append(mato.copy())
        matolista[i]["x"] = randx
        matolista[i]["y"] = randy + 500
    sorsat = lkm - 6
    peli["laatikot"] = laatikkolista
    return laatikkolista, matolista, sorsat

def tuo_kartta(tiedosto):
    """
    Lataa kartan tiedot tiedostosta
    """
    with open(tiedosto, "r") as kohde:
        tieto = json.load(kohde)
        laatikkolista = tieto["laatikot"]
        matolista = tieto["matolista"]
        sorsat = tieto["sorsat"]

    return laatikkolista, matolista, sorsat

            

def kartta(karttanro):
    """
    Lataa kartan json tiedostosta ja palauttaa laatikot, madot sekä sorsien lkm.
    """
    laatikkolista, matolista, sorsat = tuo_kartta("kartta"+str(karttanro)+".json")
    peli["laatikot"] = laatikkolista
    peli["matolista"] = matolista
    return laatikkolista, matolista, sorsat
    
def random_kartta():
    """
    Luo random kartan.
    """
    luku = random.randint(7, 10)
    kentta = luo_laatikot(luku, 200)
    return kentta


def pudota(laatikot):

    """
    Pudottaa annetussa listassa olevia neliskanttisia objekteja (määritelty
    sanakirjana jossa vasemman alakulman x, y -koordinaatit, leveys, korkeus sekä
    nopeus pystysuuntaan). Funktio pudottaa laatikoita yhtä aikayksikköä
    vastaavan matkan.
    """

    lista = sorted(laatikot, key=lambda d: d['y']+d['h'])
    for indeksi in range(0, len(lista)):
        touch = 0
        x = lista[indeksi]["x"]
        y = lista[indeksi]["y"]
        nopeus = lista[indeksi]["vy"]
        w = lista[indeksi]["w"]
        h = lista[indeksi]["h"]
    
        if y - nopeus <= 0:
            lista[indeksi]["vy"] = 0
            lista[indeksi]["y"] = 0
            touch = 1
            continue
        
        for i in reversed(range(indeksi)):
            #Alla olevan laatikon koordinaatit:
            x_2 = lista[i]["x"]
            y_2 = lista[i]["y"]
            w_2 = lista[i]["w"]
            h_2 = lista[i]["h"]
            if lista[indeksi]["y"]-lista[indeksi]["vy"]<=y_2+h_2 and not (x+w<=x_2 or x>=x_2+w_2):
                touch = 1
                lista[indeksi]["vy"] = 0
                lista[indeksi]["y"] = lista[i]["y"]+lista[i]["h"]
                break
        if touch == 0:
            lista[indeksi]["y"] -= lista[indeksi]["vy"]
            lista[indeksi]["vy"] += PUTOAMISKIIHTYVYYS

    
def piirra():
    """
    Piirtää kaikki kentällä olevat laatikot näkyviin.
    """
    
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for i in range(len(peli["laatikot"])):
        haravasto.lisaa_piirrettava_ruutu(" ", peli["laatikot"][i]["x"], peli["laatikot"][i]["y"])
    haravasto.piirra_ruudut()

def paivita(kulunut_aika):
    """
    Päivittaaa ohjelman
    """
    pudota(peli["laatikot"])

if __name__ == "__main__":
    print("PELI ALKAA")
    luo_laatikot(10,20)
    #pudota(testilista)
    haravasto.lataa_kuvat("spritet")
    haravasto.lataa_sorsa("spritet")
    haravasto.luo_ikkuna(leveys=IKKUNAN_LEVEYS, korkeus=IKKUNAN_KORKEUS)
    haravasto.aseta_piirto_kasittelija(piirra)
    haravasto.aseta_toistuva_kasittelija(paivita)
    haravasto.aloita()
