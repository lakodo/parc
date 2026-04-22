# parc

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

## Quick start

### Inspect a single unit

```python
from parc.configs.edf.sites.nuc.belleville import BEL1

print(BEL1.name)    # bel1
print(BEL1.power)
print(BEL1.design)  # FrenchNuclearUnitDesign.PP4
```

### Browse an entire grid

```python
from parc.configs.edf.france import FRENCH_GRID
from parc.constants import UnitTechnology

for site in FRENCH_GRID.sites:
    for unit in site.units:
        if unit.technology == UnitTechnology.NUCLEAR:
            print(site, "→", unit)
```

### Query units by design

```python
from parc.configs.edf.types import FrenchNuclearUnit

print(f"900 MW series : {len(FrenchNuclearUnit.get_900())} units")
print(f"1300 MW series: {len(FrenchNuclearUnit.get_1300())} units")
print(f"1450 MW series: {len(FrenchNuclearUnit.get_1450())} units")
print(f"1600 MW series: {len(FrenchNuclearUnit.get_1600())} units")
```

## CLI tools

`ecs-inspect` is a command-line tool to work with [ECS](https://en.wikipedia.org/wiki/KKS_Power_Plant_Classification_System)-style references found in documents or free text.

### Extract references from a string

```bash
ecs-inspect extract "check valve ASG021EC1 and pump RCV001PO"
```

### Extract references from a file

```bash
ecs-inspect extract-file report.txt
```

### Validate a reference

```bash
ecs-inspect validate ASG021EC1
```

```text
Query: ASG021EC1
Normalized: ASG021EC1
Exact Match: yes
Candidates: 1
Truncated: no
...
```

## Sources

All information in this library is public. Contributors should quote their public sources in the codebase when sharing information.

## Useful resources

- [RTE éCO2mix](https://www.rte-france.com/eco2mix)
- [Electricity Maps](https://app.electricitymaps.com/)

## About the author

I'm PhD Joris GUERRY, research engineer at EDF (Électricité de France). Check out my [LinkedIn profile](https://linkedin.com/in/jorisguerry) for more.

## Links

- **GitHub**: <https://github.com/lakodo/parc/>
- **Documentation**: <https://lakodo.github.io/parc/>
