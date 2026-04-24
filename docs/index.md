# parc

![parc hero showing a connected electric grid panorama with nuclear, hydro, solar, wind, substations, and transmission lines](assets/images/parc-social-card.png)

[![Release](https://img.shields.io/github/v/release/lakodo/parc)](https://img.shields.io/github/v/release/lakodo/parc)
[![Build status](https://img.shields.io/github/actions/workflow/status/lakodo/parc/main-dev.yml?branch=dev)](https://github.com/lakodo/parc/actions/workflows/main-dev.yml?query=branch%3Adev)
[![codecov](https://codecov.io/gh/lakodo/parc/branch/main/graph/badge.svg)](https://codecov.io/gh/lakodo/parc)
[![Commit activity](https://img.shields.io/github/commit-activity/m/lakodo/parc)](https://img.shields.io/github/commit-activity/m/lakodo/parc)
[![License](https://img.shields.io/github/license/lakodo/parc)](https://img.shields.io/github/license/lakodo/parc)

A model of Earth electric grid, from France to Japan, from nuclear plants to solar panel farms, from average power per site up to pressure in a pipe.

## Motivation

> How to compare French production to Italy production?
>
> How to compute the monthly average renewable energy of Europe against USA?
>
> What about EDF performance against RWE?
>
> Any idea about the impact of quitting nuclear energy in Germany?
>
> What hardware is used on prem here and there?

To answer these questions we need to represent our international grid on a common structure. I found none, so here is **parc** — an open source Python library to store, structure, and deliver public information about all electricity production systems.

## Installation

Install the latest version directly from GitHub with `uv`:

```bash
uv add git+https://github.com/lakodo/parc.git
```

Install a specific branch:

```bash
uv add git+https://github.com/lakodo/parc.git@dev
```

## Use with `uv` without installing

Run `ecs-inspect` directly from GitHub without adding anything to your environment:

=== "Code"

    ```bash
    uv run --with git+https://github.com/lakodo/parc.git ecs-inspect extract "check valve ASG021EC1 and pump RCV001PO"
    ```

=== "Result"

    ```text
    ASG021EC1
    RCV001PO-
    ```

You can also pipe the extracted references into `validate`:

=== "Code"

    ```bash
    uv run --with git+https://github.com/lakodo/parc.git ecs-inspect extract "check valve ASG021EC1 and pump RCV001PO" | xargs -I {} uv run --with git+https://github.com/lakodo/parc.git ecs-inspect validate {}
    ```

=== "Result"

    ```text
    Query: ASG021EC1
    Normalized: ASG021EC1
    Exact Match: yes
    Candidates: 1
    Truncated: no

    - type: rf
      raw: ASG021EC1
      canonical: ASG021EC1
      span: 0-9
      system: ASG
      system_label: Alimentation auxiliaire de secours des GV
      identification: 021
      base_function: 0
      order: 21
      material: EC1
      material_qualifier_meanings: Enclenché
      decomposition:
        tranche_segment: <absent> -> Tranche non précisée
        system_segment: ASG -> Alimentation auxiliaire de secours des GV
        system_letter_1: A -> Alimentation en eau - poste d'eau
        system_letters_2_3: SG -> Partie spécifique du trigramme système
        identification_segment: 021 -> Format compact sans sous-fonction
        identification_digit_1: 0 -> Fonction de base
        identification_digits_2_3: 21 -> Ordre 21
        material_segment: EC1
        material_bigram: EC
        material_qualifier: 1 -> Enclenché
    Query: RCV001PO-
    Normalized: RCV001PO-
    Exact Match: yes
    Candidates: 1
    Truncated: no

    - type: rf
      raw: RCV001PO-
      canonical: RCV001PO-
      span: 0-9
      system: RCV
      system_label: Contrôle chimique et volumétrique
      identification: 001
      base_function: 0
      order: 1
      material: PO-
      material_labels: Pompe
      decomposition:
        tranche_segment: <absent> -> Tranche non précisée
        system_segment: RCV -> Contrôle chimique et volumétrique
        system_letter_1: R -> Réacteur
        system_letters_2_3: CV -> Partie spécifique du trigramme système
        identification_segment: 001 -> Format compact sans sous-fonction
        identification_digit_1: 0 -> Fonction de base
        identification_digits_2_3: 01 -> Ordre 1
        material_segment: PO-
        material_bigram: PO -> Pompe
        material_qualifier: - -> Qualificatif absent ou non précisé
    ```

## Quick start

### Inspect a single unit

=== "Code"

    ```python
    from parc.configs.edf.sites.nuc.belleville import BEL1

    print(BEL1.name)
    print(BEL1.power)
    print(BEL1.design)
    ```

=== "Result"

    ```text
    bel1
    1300
    FrenchNuclearUnitDesign.PP4
    ```

### Browse an entire grid

=== "Code"

    ```python
    from parc.configs.edf.france import FRENCH_GRID
    from parc.constants.constants import UnitTechnology

    nuclear_units = (
        (site, unit)
        for site in FRENCH_GRID.sites
        for unit in site.units
        if unit.technology == UnitTechnology.NUCLEAR
    )

    for index, (site, unit) in enumerate(nuclear_units):
        if index == 5:
            break
        print(site, "->", unit)
    ```

=== "Result"

    ```text
    <site: "Belleville-sur-Loire" (2 units)> -> <☢️ FrenchNuclearUnitDesign.PP4 (1300): bel1 >
    <site: "Belleville-sur-Loire" (2 units)> -> <☢️ FrenchNuclearUnitDesign.PP4 (1300): bel2 >
    <site: "Blayais" (4 units)> -> <☢️ FrenchNuclearUnitDesign.CP1 (900): bla1 >
    <site: "Blayais" (4 units)> -> <☢️ FrenchNuclearUnitDesign.CP1 (900): bla2 >
    <site: "Blayais" (4 units)> -> <☢️ FrenchNuclearUnitDesign.CP1 (900): bla3 >
    ```

### Query units by design

=== "Code"

    ```python
    from parc.configs.edf.types import FrenchNuclearUnit

    print(f"900 MW series : {len(FrenchNuclearUnit.get_900())} units")
    print(f"1300 MW series: {len(FrenchNuclearUnit.get_1300())} units")
    print(f"1450 MW series: {len(FrenchNuclearUnit.get_1450())} units")
    print(f"1600 MW series: {len(FrenchNuclearUnit.get_1600())} units")
    ```

=== "Result"

    ```text
    900 MW series : 32 units
    1300 MW series: 20 units
    1450 MW series: 4 units
    1600 MW series: 1 units
    ```

## CLI tools

`ecs-inspect` is a command-line tool to work with
[EDF Coding System (ECS)](https://www.edfenergy.com/sites/default/files/introduction_to_the_safety_security_and_environmental_report.pdf)
references found in documents or free text.

### Extract references from a string

=== "Code"

    ```bash
    ecs-inspect extract "check valve ASG021EC1 and pump RCV001PO"
    ```

=== "Result"

    ```text
    ASG021EC1
    RCV001PO-
    ```

### Extract references from a file

```bash
ecs-inspect extract-file report.txt
```

### Validate a reference

=== "Code"

    ```bash
    ecs-inspect validate ASG021EC1
    ```

=== "Result"

    ```text
    Query: ASG021EC1
    Normalized: ASG021EC1
    Exact Match: yes
    Candidates: 1
    Truncated: no

    - type: rf
      raw: ASG021EC1
      canonical: ASG021EC1
      span: 0-9
      system: ASG
      system_label: Alimentation auxiliaire de secours des GV
      identification: 021
      base_function: 0
      order: 21
      material: EC1
      material_qualifier_meanings: Enclenché
      decomposition:
        tranche_segment: <absent> -> Tranche non précisée
        system_segment: ASG -> Alimentation auxiliaire de secours des GV
        system_letter_1: A -> Alimentation en eau - poste d'eau
        system_letters_2_3: SG -> Partie spécifique du trigramme système
        identification_segment: 021 -> Format compact sans sous-fonction
        identification_digit_1: 0 -> Fonction de base
        identification_digits_2_3: 21 -> Ordre 21
        material_segment: EC1
        material_bigram: EC
        material_qualifier: 1 -> Enclenché
    ```

## Sources

All information in this library is public. Contributors should quote their public sources in the codebase when sharing information.

## Useful resources

- [RTE éCO2mix](https://www.rte-france.com/eco2mix)
- [Electricity Maps](https://app.electricitymaps.com/)

## About the author

I'm PhD Joris GUERRY, research engineer at EDF (Électricité de France) until June 2026. Check out my [LinkedIn profile](https://linkedin.com/in/jorisguerry) for more.

## Links

- **GitHub**: <https://github.com/lakodo/parc/>
- **Documentation**: <https://lakodo.github.io/parc/>
