#Partie 2.1

"""
Imaginez un réseau informatique comme un vaste réseau routier traversant le monde,
permettant aux informations de circuler à la vitesse de l'éclair. Ce réseau routier,
c'est ce qu'on appelle le backbone, l'épine dorsale de l'internet.

Notre mission ? Simuler ce backbone, reproduire ses complexités et ses merveilles
en utilisant le pouvoir du code. Nous allons créer des nœuds, les villes numériques
de ce réseau, et les relier par des arêtes, les autoroutes de l'information.

Mais attention, ce n'est pas n'importe quel réseau ! Notre backbone sera digne
des plus grands ingénieurs, avec des connexions hiérarchisées et des algorithmes
intelligents pour trouver les chemins les plus courts.

En fin de compte, nous pourrons visualiser ce chef-d'œuvre numérique, admirer
les flux de données qui traversent ses veines virtuelles et comprendre comment
l'information circule à travers le monde.

Alors, prêts à plonger dans cet univers fascinant de code et de réseaux ?
Accrochez-vous bien, car ce projet va vous faire voyager !
"""

class Sommets(object):
    def __init__(self, name):
        self.name = name
        self.temps = float('inf')
        self.precedent = None

class Aretes(object):
    def __init__(self, depart, arrivee, temps, name, Gold):
        self.depart = depart
        self.arrivee = arrivee
        self.temps = temps
        self.name = name
        self.GolDRoger = Gold


class Graph(object):
    def __init__(self):
        self.sommets = []
        self.arretes = []

    def ajouter_sommet(self, sommet):
        self.sommets.append(sommet)

    def ajouter_arete(self, arete):
        self.arretes.append(arete)

    def afficher_graph(self):
        for arete in self.arretes:
            print(arete.depart.name, "->", arete.arrivee.name)


    def dijkstra(self, depart, arrivee, niveau):
        """recupere les objects depart et arrivee et
        retourne le chemin le plus cours ainsi que le
        temps

        Args:
            depart (Object): depart.sommet
            arrivee (Object): depart.arrivee

        Returns:
            List: le chemin de la distance la plus courte
            int: le temps que prendra le chemin
        """
        # Initialisation
        for sommet in self.sommets:
            sommet.temps = float('inf')
            sommet.precedent = None

        chemin_arete = []
        depart.temps = 0

        # Algorithme de Dijkstra
        sommets_non_traites = list(self.sommets)
        while sommets_non_traites:
            sommet_courant = min(sommets_non_traites, key=lambda s: s.temps)
            if sommet_courant == arrivee:
                break
            sommets_non_traites.remove(sommet_courant)
            for arete in self.arretes:
                if arete.depart == sommet_courant:
                    temps = sommet_courant.temps + arete.temps[niveau]
                    if temps < arete.arrivee.temps:
                        if len(chemin_arete):
                            for item in chemin_arete:
                                if item.arrivee == arete.arrivee:
                                    chemin_arete.remove(item)
                        arete.arrivee.temps = temps
                        arete.arrivee.precedent = sommet_courant
                        chemin_arete.append(arete)

        # Construction du chemin
        chemin = []
        sommet_courant = arrivee
        while sommet_courant.precedent is not None:
            chemin.insert(0, sommet_courant)
            sommet_courant = sommet_courant.precedent
            for arete in chemin_arete:
                if arete.arrivee == sommet_courant:
                    chemin.insert(0, arete)
                    arete.GolDRoger = 1
                    break
        chemin.insert(0, sommet_courant)



        # Retour du résultat
        return chemin, arrivee.temps

    def afficher_chemin(self, chemin, temps):
        print(f'le chemin le plus rapide prend {temps} secondes')
        print(f'On commence par partir de {chemin[0]}.name')
        counter = 0
        for i in range(1, len(chemin)-1, 2):
            print(f"On passe par {chemin[i].name} jusqu'à {chemin[i+1].name}")
            counter += 1
        print('On est arrivés en passant par', counter, 'arêtes')