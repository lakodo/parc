"""EDF ECS material codes and helpers.

Source: ``[28] ENSIRM0100021 A - Codification ECS.pdf``.
"""

from dataclasses import dataclass
from types import MappingProxyType

MATERIAL_CODE_LABELS = MappingProxyType({
    "AA": ("Alarme conventionnelle",),
    "AC": ("Ascenseur", "Monte-charge"),
    "AD": ("Absorbeur",),
    "AE": ("Aérotherme",),
    "AG": ("Agitateur", "Vibreur"),
    "AI": ("Armoire incendie",),
    "AK": ("Point d'ancrage",),
    "AM": ("Amplificateur",),
    "AN": ("Alimentation stabilisée",),
    "AO": ("Anode",),
    "AP": ("Alternateur",),
    "AQ": ("Accumulateur fluide autre qu'électrique",),
    "AR": ("Armoire", "Armoire de distribution"),
    "AS": ("Assemblages combustibles",),
    "AU": ("Dispositif d'arrêt d'urgence",),
    "AV": ("Avaloir (eaux pluviales)",),
    "BA": (
        "Bâche",
        "Bouteille de gaz",
        "Bouteille tampon sur prise de pression",
        "Cuve",
        "Fosse septique",
        "Puisard",
        "Réservoir",
    ),
    "BC": ("Boîte de connexion (bloc essai)",),
    "BF": ("Borne fontaine", "Bouche d'arrosage", "Rampe d'aspersion", "Sprinkler"),
    "BH": ("Bouche d'aération", "Bouche d'air et d'extraction"),
    "BJ": ("Borne incendie", "Bouche incendie", "Poteau incendie"),
    "BK": ("Mécanisme des grappes", "Unité de commande de barres"),
    "BM": ("Injecteur",),
    "BN": ("Bornier", "Répartiteur"),
    "BO": ("Bouchon",),
    "BQ": ("Bloc sécurité (éclairage secours)",),
    "BR": ("Barres de contrôle et de sécurité",),
    "BS": ("Boîte de soudure froide",),
    "BT": ("Accumulateur électrique", "Batterie"),
    "BU": ("Batardeau",),
    "BV": ("Boîtier de voyants",),
    "BW": ("Refoulement d'air et de soufflage",),
    "BY": ("Broyeur",),
    "BZ": ("Caisson",),
    "CA": ("Câble",),
    "CB": ("Capacité", "Condensateur"),
    "CC": ("Commande de choix",),
    "CD": ("Commande diverse",),
    "CE": ("Composant électrique",),
    "CF": ("Centrifugeuse",),
    "CG": ("Commande calculateur logique", "Commande groupé logique", "Commande logique de fonction"),
    "CH": ("Chaudière", "Générateur de vapeur"),
    "CI": ("Commande individuelle logique",),
    "CK": ("Commande de grappe",),
    "CL": ("Armoire de climatisation", "Climatiseur"),
    "CM": ("Serrure",),
    "CN": ("Colonne (appareil)",),
    "CO": ("Compresseur", "Surpresseur"),
    "CP": ("Coupleur (hydraulique ou mécanique)",),
    "CQ": ("Chassis",),
    "CR": ("boîtier d'essai PTT (en coffret)", "Coffret"),
    "CS": ("Condenseur",),
    "CU": ("Cuvelage",),
    "CV": ("Caniveau",),
    "CW": ("Commande d'appoint primaire",),
    "CY": ("Cheminée",),
    "DA": ("Dispositif auto bloquant",),
    "DB": ("Amortisseur",),
    "DD": ("Cheminée de désurchauffe", "Chemise de désurchauffe", "Tuyère de désurchauffe"),
    "DE": ("Déminéraliseur", "Désioniseur"),
    "DG": ("Dégrilleur",),
    "DH": ("Déshuileur",),
    "DI": ("Diaphragme (autre que ceux de mesure)", "Limiteur de débit", "Obturateur", "Tuyère", "Venturi"),
    "DJ": ("Emetteur/Récepteur infra-rouge",),
    "DK": ("Disque de rupture (membrane déchirable)",),
    "DL": ("Onduleur",),
    "DM": ("Connexion des dispositifs mobiles",),
    "DR": ("Distributeur (tiroir)",),
    "DS": ("Déshydratant", "Dessicateur", "Sécheur"),
    "DT": ("Cellule photo électrique", "Détecteur"),
    "DV": ("Distributeur vibrant",),
    "DX": ("Dépoussiéreur",),
    "DZ": ("Dégazeur",),
    "EA": ("Electroaimant",),
    "EB": ("Electrolyseur",),
    "EE": ("Electro d'embrayage",),
    "EG": ("Mélangeur",),
    "EJ": ("Ejecteur",),
    "EL": ("Electrovanne pilote (uniquement pour plusieurs vannes)",),
    "EN": ("Courbe sur écran", "Enregistreur"),
    "EP": ("Convertisseur électropneumatique (uniquement pour plusieurs vannes)",),
    "ER": ("Electrofrein",),
    "ES": ("Appareils d'éclairage",),
    "ET": ("Extracteur",),
    "EU": ("Humidificateur d'air",),
    "EV": ("Evaporateur",),
    "EW": ("Electrode de référence (mesure PH)",),
    "EX": ("Echangeur",),
    "EZ": ("Extincteur",),
    "FA": ("Fiche d'alarme",),
    "FI": ("Filtre", "Pré filtre"),
    "FL": ("Flexible",),
    "FO": ("Fibre optique",),
    "FP": ("Fond plein",),
    "FU": ("Fusible",),
    "FX": ("Dispositif de fixation", "Point fixe d'accrochage"),
    "GA": ("Générateur de courant alternatif",),
    "GC": ("Générateur de courant continu",),
    "GD": ("Générateur de fonction",),
    "GE": ("Groupe électrogène",),
    "GF": ("Groupe frigorifique",),
    "GL": ("Gaine de ventilation",),
    "GM": ("Générateur de mousse",),
    "GR": ("Graisseur", "Lubrificateur"),
    "GS": ("Siphon", "Siphon de sol"),
    "GT": ("Entonnoir", "Gate"),
    "GU": ("Générateur ultrasons",),
    "HA": ("Lampe", "LED", "Voyant"),
    "HB": ("Boule roulante", "Souris"),
    "HC": ("Calculateur", "Micro ordinateur", "Microprocesseur", "Unité centrale"),
    "HD": ("afficheur", "Bargraphe", "Indicateur"),
    "HE": ("Instrumentation",),
    "HI": ("Imprimante", "Télescriptrice", "Télex"),
    "HK": ("Clavier fonctionnel", "Console système"),
    "HL": ("Lecteur de badges", "Lecteur de Bande", "Streamer"),
    "HN": ("Liaison fil à fil",),
    "HP": ("Pot de visualisation",),
    "HQ": ("Demultiplexeur", "Multiplexeur"),
    "HR": ("Horloge",),
    "HS": ("Indicateur de circulation",),
    "HT": ("Interphonie", "Moyens de communication"),
    "HV": ("Ecran",),
    "HW": ("Antenne",),
    "HX": ("Alarme sonore", "Klaxon"),
    "HY": ("Modem", "Transceiver"),
    "JA": ("Appareil de coupure électrique", "Contacteur", "Disjoncteur"),
    "JB": ("Jeu de barres",),
    "JC": ("Cellule électrique",),
    "JO": ("Joint", "Joint de dilatation"),
    "JP": ("Pont de barre",),
    "JQ": ("Contacteur statique",),
    "JR": ("Réserve 380 V et 6,6 kV",),
    "JS": ("Sectionneur",),
    "JT": ("Sectionneur de mise à la terre",),
    "JW": ("Parafoudre",),
    "KA": ("Alarme sur écran",),
    "KD": ("Orifice déprimogène de mesure de débit",),
    "KI": ("Crépine",),
    "KM": ("Information analogique élaborée",),
    "KR": ("Cryogénérateur",),
    "KS": ("Information logique élaborée",),
    "KT": ("Elément primaire de température",),
    "LA": ("Chariot de manutention",),
    "LB": ("Câble de levage",),
    "LC": ("Potence",),
    "LD": ("Dispositif de chargement et de manutention",),
    "LF": ("Fer de roulement", "Poutre de manutention", "Rail"),
    "LG": ("Grappin",),
    "LI": ("Trappe de manutention",),
    "LM": ("Moufle",),
    "LP": ("Palan", "Treuil"),
    "LR": ("Pont", "Pont roulant", "Portique"),
    "LT": ("Tapis de transfert", "Transfert", "Transporteur"),
    "MA": ("Mesure d'activité", "Mesure de flux", "Mesure de rayonnement"),
    "MC": ("Mesure de vitesse",),
    "MD": ("Mesure de débit",),
    "ME": ("Mesure acoustique",),
    "MF": ("Mesure de fréquence", "Mesure de phase"),
    "MG": ("Mesure d'analyse physico-chimique",),
    "MH": ("Mesure de temps",),
    "MI": ("Mesure d'intensité",),
    "MJ": ("Détecteur incendie",),
    "ML": ("Mesure d'opacité", "Mesure de luminosité"),
    "MM": ("Mesure de déplacement", "Mesure de position"),
    "MN": ("Mesure de niveau",),
    "MO": ("Moteur (uniquement pour les actionneurs à moteur multiple)",),
    "MP": ("Mesure de pression",),
    "MQ": ("Mesure de puissance réactive",),
    "MR": ("Mesure d'impédance", "Mesure de conductivité", "Mesure de résistance", "Mesure de résistivité"),
    "MS": ("Mesure santé",),
    "MT": ("Mesure de température",),
    "MU": ("Mesure de tension",),
    "MV": ("Mesure de dilatation", "Mesure de poussée", "Mesure de séisme", "Mesure de vibration"),
    "MW": ("Mesure de puissance active",),
    "MX": ("Mesure divers mécanique",),
    "MY": ("Mesure divers électrique",),
    "MZ": ("Mesure divers physique",),
    "NA": ("Nacelle",),
    "ND": ("Nœud",),
    "NE": ("Fonction de base",),
    "NF": ("Sous-fonction",),
    "NL": ("Liaison fonctionnelle",),
    "PB": ("Piège à son", "Silencieux"),
    "PE": ("Postiche élément combustible",),
    "PG": ("Pompe électromagnétique",),
    "PI": ("Poste incendie",),
    "PJ": ("Connecteur", "Prise", "Prise informatique"),
    "PL": ("Palier",),
    "PN": ("Piston", "Vérin"),
    "PO": ("Pompe",),
    "PP": ("Pupitre",),
    "PQ": ("Presse à compacter",),
    "PT": ("Strap",),
    "PU": ("Purgeur",),
    "PX": ("Poste examen du combustible",),
    "QA": ("Compteur d'activité",),
    "QC": ("Compte tour",),
    "QD": ("Compteur volumétrique",),
    "QH": ("Compteur de temps",),
    "QM": ("Compteur de manœuvres",),
    "QN": ("Compteur numérique",),
    "QQ": ("Compteur d'énergie réactive",),
    "QW": ("Compteur d'énergie active",),
    "QX": ("Compteur d'événements",),
    "RA": ("Registre d'air (isolement ou réglage)",),
    "RB": ("Rampe de bouteilles",),
    "RD": ("Redresseur",),
    "RE": ("Réchauffeur non électrique",),
    "RF": ("Batterie froide", "Réfrigérant", "Refroidisseur d'air"),
    "RG": ("Commande réglante groupée",),
    "RI": ("Commande réglante individuelle",),
    "RJ": ("Raccord incendie",),
    "RK": ("Rack",),
    "RP": ("Refroidisseur de purges ou de condensats",),
    "RR": ("Multiplicateur de vitesse", "Réducteur de vitesse", "Variateur de vitesse"),
    "RS": ("Convecteur", "Elément de préchauffage", "Réchauffeur électrique", "Résistance chauffante"),
    "RV": ("Recombineurs d'hydrogène",),
    "RW": ("Répéteur multiport (HUB)",),
    "RX": ("Régime (de consignation, d'essai...)",),
    "RY": ("Manchette démontable", "Raccord par bride"),
    "SA": ("TOR neutronique d'activité - flux",),
    "SC": ("TOR de vitesse",),
    "SD": ("Contrôleur de circulation", "TOR de débit"),
    "SE": ("TOR acoustique",),
    "SF": ("TOR de fréquence - phase",),
    "SG": ("TOR d'analyse physico-chimique",),
    "SH": ("TOR détecteur à seuil d'humidité",),
    "SI": ("TOR d'intensité",),
    "SJ": ("TOR détecteur d'incendie",),
    "SK": ("TOR de contrainte",),
    "SL": ("TOR de luminosité",),
    "SM": ("Fin de course (PMC)", "TOR de déplacement", "TOR de position"),
    "SN": ("TOR de niveau",),
    "SP": ("TOR de pression",),
    "SR": ("TOR d'impédance", "TOR de conductivité", "TOR de résistance"),
    "SS": ("TOR de santé",),
    "ST": ("Thermostat", "TOR de température"),
    "SU": ("TOR de présence tension",),
    "SV": ("TOR de dilatation", "TOR de poussée", "TOR de vibration"),
    "SX": ("TOR divers mécanique",),
    "SY": ("Information TOR venant de la régulation", "TOR divers électrique"),
    "SZ": ("TOR divers physique",),
    "TA": ("Transformateur auxiliaire réseau",),
    "TB": ("Tableau",),
    "TC": ("Turbine",),
    "TF": ("Grilles filtrantes", "Tambours filtrants"),
    "TH": ("Thermocouple",),
    "TI": ("Transformateur d'intensité",),
    "TO": ("Bouton poussoir", "Commutateur aveugle", "Mécanisme de verrouillage à clé", "Touche"),
    "TP": ("Transformateur principal",),
    "TR": ("Transformateur de puissance",),
    "TS": ("Transformateur de soutirage",),
    "TT": ("Puits de terre", "Regard de terre"),
    "TU": ("Transformateur de tension",),
    "TV": ("Auto-transformateur de puissance",),
    "TW": ("Traversée",),
    "TX": ("Transformateur de vapeur",),
    "TY": ("Tuyauterie",),
    "UP": ("Unité de polarité",),
    "UR": ("Platine relais", "Unité de relayage"),
    "US": ("Unité d'isolement",),
    "UU": ("Variateur de tension",),
    "VA": ("Vanne d'air",),
    "VB": ("Vanne eau borée et non primaire",),
    "VC": ("Vanne eau de circulation",),
    "VD": ("Vanne eau déminéralisée",),
    "VE": ("Vanne eau brute",),
    "VF": ("Vanne combustible principal",),
    "VG": ("Vanne CO2- gaz divers",),
    "VH": ("Vanne d'huile",),
    "VI": ("Vanne d'air de ventilation",),
    "VJ": ("Vanne effluents gazeux",),
    "VK": ("Vanne effluents liquides",),
    "VL": ("Vanne eau de condensation",),
    "VM": ("Vanne combustible d'allumage (propane - mazout)",),
    "VN": ("Vanne eau de circuit Noria",),
    "VP": ("Vanne eau primaire",),
    "VQ": ("Vanne liquide organique",),
    "VR": ("Vanne réactif",),
    "VS": ("Vanne effluents solides (boues, suies ...)",),
    "VT": ("Vanne eau potable - eau de nappe",),
    "VV": ("Vanne vapeur",),
    "VX": ("Vanne argon",),
    "VY": ("Vanne hydrogène",),
    "VZ": ("Vanne azote",),
    "WB": ("Volet bas (cellule)",),
    "WH": ("Volet haut (cellule)",),
    "WM": ("Electroménager",),
    "WN": ("Télémanipulateur",),
    "WO": ("Machine-outil", "Outillage"),
    "WV": ("Raccord rapide",),
    "XB": ("Relais bistable",),
    "XC": ("Relais à contact de passage",),
    "XH": ("Relais de fréquence",),
    "XI": ("Relais d'intensité",),
    "XK": ("Relais de défaut",),
    "XP": ("Relais d'antipompage",),
    "XR": (
        "Relais duplex radio (émetteur-récepteur)",
        "Relais instantanés autres que définis dans ce tableau (répétiteurs..)",
    ),
    "XS": ("Relais de surcharge",),
    "XT": ("Relais auxiliaire temporisé (cas général)",),
    "XU": ("Relais de tension", "Relais voltmétrique"),
    "XW": ("Relais de puissance",),
    "XZ": ("Relais de détection de terre",),
    "YC": ("Image de conduite",),
    "YE": ("Image de suivi d'équipement",),
    "YM": ("Image menu",),
    "YP": ("Image de procédure",),
    "YR": ("Renvoi fléché",),
    "YS": ("Image de suivi de situation",),
    "ZD": ("Soufflet de dilatation",),
    "ZE": ("Séparateur",),
    "ZF": ("Surchauffeur (quand séparé du sécheur)",),
    "ZI": ("Silencieux",),
    "ZK": ("Synchrocoupleur",),
    "ZM": ("Servomoteur",),
    "ZN": ("Sonde à résistance",),
    "ZO": ("Soudeuse",),
    "ZS": ("Sas",),
    "ZV": ("Soufflante", "Ventilateur"),
    "ZZ": ("Sécheur-surchauffeur",),
})

SENSOR_ANALOG_BIGRAMS = frozenset({
    "MA",
    "MC",
    "MD",
    "ME",
    "MF",
    "MG",
    "MH",
    "MI",
    "MJ",
    "ML",
    "MM",
    "MN",
    "MP",
    "MQ",
    "MR",
    "MS",
    "MT",
    "MU",
    "MV",
    "MW",
    "MX",
    "MY",
    "MZ",
})
SENSOR_TOR_BIGRAMS = frozenset({
    "SA",
    "SC",
    "SD",
    "SE",
    "SF",
    "SG",
    "SH",
    "SI",
    "SJ",
    "SK",
    "SL",
    "SM",
    "SN",
    "SP",
    "SR",
    "SS",
    "ST",
    "SU",
    "SV",
    "SX",
    "SY",
    "SZ",
})
CONTROL_LOCATION_QUALIFIERS = MappingProxyType({
    "P": "Moyen de conduite principal (MCP)",
    "S": "Moyen de conduite de secours (MCS)",
    "R": "Moyen de conduite de repli",
    "L": "Moyen de conduite local",
    "T": "Moyen de conduite décentralisé",
})
ACTIONNEUR_STATE_QUALIFIERS = MappingProxyType({
    "1": "Enclenché",
    "2": "Disponible",
    "3": "Vanne ouverte (sur fin de course moteur) ou actionneur enclenché",
    "4": "Vanne ouverte (sur fin de course de tige) ou matériel THT ouvert ou déclenché",
    "5": "Vanne fermée (sur fin de course moteur) ou actionneur déclenché",
    "6": "Vanne fermée (sur fin de course de tige) ou matériel THT fermé ou enclenché",
    "7": "Défaut électrique",
    "8": "Première position intermédiaire depuis l'ouverture vers la fermeture",
    "9": "Deuxième position intermédiaire depuis l'ouverture vers la fermeture",
})
MATERIAL_QUALIFIER_HINTS = MappingProxyType({
    "HA": MappingProxyType({
        "-": "Etat nominal du capteur ou de la séquence",
        "2": "Organe indisponible",
        "3": "Vanne ouverte (sur fin de course moteur) ou actionneur enclenché",
        "4": "Vanne ouverte (sur fin de course tige)",
        "5": "Vanne fermée (sur fin de course moteur) ou actionneur déclenché",
        "6": "Vanne fermée (sur fin de course tige)",
        "7": "Défaut électrique ou défaut sur processus/séquence",
    }),
    "CA": MappingProxyType({
        "A": "Câble moyenne tension",
        "B": "Câble basse tension",
        "C": "Câble de contrôle",
        "F": "Câble informatique",
        "H": "Câble haute tension",
        "I": "Câble interphone",
        "M": "Liaison mesure",
        "S": "Câble de sonorisation",
        "T": "Câble téléphone",
    }),
    "BN": MappingProxyType({
        "D": "Raccordements divers",
        "E": "Electrique",
        "I": "Informatique",
        "T": "Raccordement PTT",
    }),
    "BC": MappingProxyType({
        "D": "Raccordements divers",
        "E": "Electrique",
        "I": "Informatique",
        "T": "Raccordement PTT",
    }),
    "PJ": MappingProxyType({
        "D": "Raccordements divers",
        "E": "Electrique",
        "I": "Informatique",
        "T": "Raccordement PTT",
    }),
    "DT": MappingProxyType({"H": "Hyper fréquence", "I": "Infrarouge", "J": "Incendie"}),
    "CE": MappingProxyType({
        "C": "Condensateur",
        "D": "Diode ou thyristor",
        "L": "Self ou inductance",
        "R": "Résistance, potentiomètre ou shunt",
        "T": "Télérupteur",
    }),
    "HE": MappingProxyType({
        "C": "Chromatographe",
        "K": "Convertisseur électrique ou changeur de fréquence",
        "O": "Oscilloperturbographe",
        "T": "Tachyperturbographe",
    }),
    "HT": MappingProxyType({
        "B": "Recherche de personnes / beeper",
        "G": "Généphone",
        "I": "Interphone",
        "L": "Haut parleur",
        "M": "Microphone",
        "T": "Téléphone",
        "Y": "Radio / talkie walkie",
        "Z": "Téléphone de sûreté",
    }),
    "TW": MappingProxyType({"E": "Traversée extérieure gauche", "I": "Traversée intérieure gauche"}),
    "FL": MappingProxyType({"P": "Flexible provisoire"}),
    "FP": MappingProxyType({"P": "Fond plein provisoire"}),
    "PT": MappingProxyType({"P": "Strap provisoire"}),
    "TY": MappingProxyType({"B": "Branche de tuyauterie"}),
    "GL": MappingProxyType({"B": "Branche de gaine de ventilation"}),
    "FI": MappingProxyType({
        "A": "Filtre de très haute efficacité (absolu)",
        "D": "Filtre provisoire / filtre de démarrage",
        "F": "Filtre de très haute efficacité (fin)",
        "I": "Piège à iode",
        "P": "Filtre de moyenne efficacité (préfiltre)",
    }),
    "JO": MappingProxyType({
        "E": "Joint d'étanchéité à presse étoupe",
        "G": "Joint d'étanchéité à garniture mécanique",
        "I": "Joint isolant",
        "J": "Joint plein",
    }),
    "BA": MappingProxyType({
        "B": "Ballon",
        "N": "Bouteille de niveau",
        "P": "Trou d'homme",
        "T": "Bouteille tampon sur prise de pression",
    }),
    "RB": MappingProxyType({"G": "Bouteille de gaz"}),
    "GT": MappingProxyType({"E": "Entonnoir", "G": "Gate"}),
    "PO": MappingProxyType({"C": "Chassis", "K": "Corps", "M": "Moteur de l'organe"}),
    "ZV": MappingProxyType({"C": "Chassis", "K": "Corps"}),
    "CV": MappingProxyType({"C": "Caniveau de câble", "H": "Chambre de tirage de câble"}),
    "CM": MappingProxyType({"L": "Serrure électrique", "M": "Serrure mécanique"}),
    "BZ": MappingProxyType({
        "C": "Caisson de batterie froide",
        "F": "Caisson de filtre",
        "H": "Caisson de réchauffeur",
    }),
    "AS": MappingProxyType({
        "A": "Absorbant",
        "C": "Couverture",
        "E": "Protection / écran",
        "F": "Combustible",
        "K": "Assemblage avec absorbant consommable",
        "L": "Restricteur de flux",
        "M": "Modérateur",
        "N": "Plénum",
        "R": "Réflecteur",
        "S": "Source de neutron",
        "X": "Assemblage spécial",
    }),
    "RX": MappingProxyType({
        "C": "Consignation",
        "E": "Essai",
        "I": "Intervention immédiate",
        "R": "Réquisition",
        "T": "Exceptionnel de travaux",
        "X": "Exploitation et lignage",
    }),
    "NL": MappingProxyType({"E": "Liaison électrique", "T": "Liaison fluide", "V": "Liaison ventilation"}),
})
TRANSFORMER_BIGRAMS = frozenset({"TA", "TI", "TP", "TR", "TS", "TU", "TV"})
IMAGE_BIGRAMS = frozenset({"YC", "YE", "YF", "YM", "YP", "YR", "YS"})
NON_ASSOCIATED_COMMAND_BIGRAMS = frozenset({"CC", "CD", "CG", "CI", "RG", "RI"})
ALARM_BIGRAMS = frozenset({"AA", "KA"})


@dataclass(frozen=True)
class MaterialCodeDescription:
    """Structured description for an ECS material code."""

    code: str
    bigram: str
    qualifier: str
    labels: tuple[str, ...]
    qualifier_meanings: tuple[str, ...]


def normalize_material_code(code: str) -> str:
    """Normalize an ECS material code."""

    return code.strip().upper().replace(" ", "")


def split_material_code(code: str) -> tuple[str, str]:
    """Split a material code into bigram and qualifier."""

    normalized = normalize_material_code(code)
    if len(normalized) == 2:
        return normalized, "-"
    if len(normalized) == 3:
        return normalized[:2], normalized[2]
    msg = f"Invalid ECS material code: {code!r}"
    raise ValueError(msg)


def describe_material_bigram(code: str) -> tuple[str, ...] | None:
    """Return labels associated with an ECS material bigram."""

    return MATERIAL_CODE_LABELS.get(normalize_material_code(code)[:2])


def _sensor_qualifier_meaning(bigram: str, qualifier: str) -> tuple[str, ...]:
    if bigram not in SENSOR_ANALOG_BIGRAMS | SENSOR_TOR_BIGRAMS:
        return ()
    sensor_meanings = {
        "-": "Capteur d'exploitation raccordé au contrôle-commande",
        "I": "Capteur intelligent",
        "L": "Capteur local",
        "Y": "Capteur d'essai",
    }
    if qualifier not in sensor_meanings:
        return ()
    return (sensor_meanings[qualifier],)


def _location_qualifier_meaning(bigram: str, qualifier: str) -> tuple[str, ...]:
    if qualifier not in CONTROL_LOCATION_QUALIFIERS:
        return ()
    if bigram in {"HD", "EN"} | NON_ASSOCIATED_COMMAND_BIGRAMS | ALARM_BIGRAMS:
        return (CONTROL_LOCATION_QUALIFIERS[qualifier],)
    return ()


def _transformer_qualifier_meaning(bigram: str, qualifier: str) -> tuple[str, ...]:
    if bigram not in TRANSFORMER_BIGRAMS or qualifier not in {"A", "B", "C"}:
        return ()
    return (
        {
            "A": "Premier enroulement secondaire",
            "B": "Deuxième enroulement secondaire",
            "C": "Troisième enroulement secondaire",
        }[qualifier],
    )


def _image_qualifier_meaning(bigram: str, qualifier: str) -> tuple[str, ...]:
    if bigram not in IMAGE_BIGRAMS or qualifier not in {"S", "O"}:
        return ()
    return (
        {
            "O": "Menu opératoire de l'image",
            "S": "Menu de sélection de l'image",
        }[qualifier],
    )


def _valve_qualifier_meaning(bigram: str, qualifier: str) -> tuple[str, ...]:
    if not bigram.startswith("V"):
        return ()
    valve_meanings = {
        "-": "Organe principal",
        "A": "Robinet amont anti-effet chaudière",
        "B": "Robinet aval anti-effet chaudière",
        "C": "Clapet distributeur 3 voies",
        "E": "Electrovanne d'ouverture",
        "H": "Electrovanne de fermeture",
        "P": "Premier isolement air",
        "Q": "Deuxième isolement air",
        "R": "Electro positionneur réglant",
        "W": "Deuxième électrovanne de la deuxième voie",
        "X": "Première électrovanne de la première voie",
        "Y": "Première électrovanne de la deuxième voie",
        "Z": "Deuxième électrovanne de la première voie",
    }
    if qualifier not in valve_meanings:
        return ()
    return (valve_meanings[qualifier],)


def _generic_actionneur_meanings(bigram: str, qualifier: str) -> tuple[str, ...]:
    meanings: list[str] = []
    if qualifier in ACTIONNEUR_STATE_QUALIFIERS:
        meanings.append(ACTIONNEUR_STATE_QUALIFIERS[qualifier])
    if qualifier == "K":
        meanings.append("Commande (volant) déportée hors du local de l'organe")
    if qualifier == "M" and bigram not in {"CM", "HT"}:
        meanings.append("Moteur de l'organe")
    return tuple(meanings)


def describe_material_qualifier(bigram: str, qualifier: str) -> tuple[str, ...]:
    """Return known meanings for the third character of a material code."""

    bigram = normalize_material_code(bigram)[:2]
    qualifier = normalize_material_code(qualifier) or "-"
    meanings: list[str] = []

    exact = MATERIAL_QUALIFIER_HINTS.get(bigram)
    if exact and qualifier in exact:
        meanings.append(exact[qualifier])

    for helper in (
        _sensor_qualifier_meaning,
        _location_qualifier_meaning,
        _transformer_qualifier_meaning,
        _image_qualifier_meaning,
        _valve_qualifier_meaning,
        _generic_actionneur_meanings,
    ):
        meanings.extend(helper(bigram, qualifier))

    deduped: list[str] = []
    for meaning in meanings:
        if meaning not in deduped:
            deduped.append(meaning)
    return tuple(deduped)


def describe_material_code(code: str) -> MaterialCodeDescription:
    """Return a structured description for an ECS material code."""

    bigram, qualifier = split_material_code(code)
    labels = MATERIAL_CODE_LABELS.get(bigram, ())
    return MaterialCodeDescription(
        code=f"{bigram}{qualifier}",
        bigram=bigram,
        qualifier=qualifier,
        labels=labels,
        qualifier_meanings=describe_material_qualifier(bigram, qualifier),
    )


def describe_extension(material_code: str, extension: str) -> tuple[str, ...]:
    """Return known meanings for a section 4 extension."""

    code = normalize_material_code(material_code)
    extension = normalize_material_code(extension)
    if not extension:
        return ()

    bigram, qualifier = split_material_code(code)
    meanings: list[str] = []

    if code == "ARC" and len(extension) == 4:
        meanings.append(f"Carte en rack {extension[:2]}, position {extension[2:]}")

    if bigram in {"TY", "GL"} and len(extension) == 4:
        component_names = {
            "C": "Cintre",
            "E": "Coude",
            "L": "Piquage",
            "S": "Point de supportage ou de fixation",
            "T": "Té",
        }
        if extension[0] in component_names:
            meanings.append(f"{component_names[extension[0]]} n°{extension[1:]}")

    if bigram == "DT" and qualifier == "J" and len(extension) == 4:
        detector_types = {"I": "Détecteur individuel", "M": "Détecteur maître", "S": "Détecteur esclave"}
        if extension[0] in detector_types:
            meanings.append(f"{detector_types[extension[0]]} {extension[1:]}")

    if bigram in SENSOR_ANALOG_BIGRAMS | SENSOR_TOR_BIGRAMS:
        sensor_extensions = {"7": "Défaut capteur", "A": "Alimentation", "I": "Première mesure", "J": "Deuxième mesure"}
        if extension[0] in sensor_extensions:
            meanings.append(sensor_extensions[extension[0]])
        elif extension[0].isdigit():
            meanings.append(f"Seuil {extension[0]}")

    return tuple(meanings)
