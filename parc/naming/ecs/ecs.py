from parc.utils.types import StrEnum


class ElementarySystems(StrEnum):
    A = " Alimentation en eau - Poste d'eau"
    B = " Manutention, stockage des combustibles et de leurs résidus (thermique à flamme uniquement)"
    C = " Condensation, refroidissement (condenseur)"
    D = " Systèmes annexes non importants pour la production (divers)"
    E = " Enceinte de confinement "
    F = " Chaudière (combustion, générateur de vapeur, thermique à flamme uniquement)"
    G = " Groupe turboalternateur et évacuation d'énergie,"
    H = " Bâtiments"
    J = " Incendie"
    K = " Contrôle"
    L = " Distribution électrique"
    P = " Piscine de stockage du combustible"
    R = " Réacteur"
    S = " Services généraux liés à la production"
    T = " Traitement des effluents"
    V = " Circuit vapeur principal"
    X = " Production vapeur auxiliaire"
    Y = " Installations d'essai "


# print(ElementarySystems["A"],ElementarySystems._member_map_.keys())
