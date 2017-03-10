# TGR Testy
## O co se jedná?
Projekt obsahuje jednoduchý testovací/validační skript, který slouží k ověření a otestování projektu do tgr. Po dodání zipu a testů, které nad ním chcete provést skript provede následující kroky:

1. Rozbalí zip do adresáře projekt
1. Ověří, zda je struktůra projektu správná (zda obsahuje všechny soubory atd...)
1. Spustí make v ./projekt
1. Nad vytvořenýmí spustitelnými soubory spustí všechny specifikované testy

## Jak to použít?
Stačí na první místo vložit název zipu a pak dodat testy, které chcete nad zipem provést. Příklad volání zde:

```
./test.py foo.zip ukol_1/A/ze_zadani.json
```
## Formát testů
Testy jsou textové soubory v jsonu. Každý test je reprezentován jedním json objektem, který může/musí obsahovat následující atributy.

| Název            |  Popis                                   | Povinný (A/N) |
|------------------|------------------------------------------|---------------|
|jmeno             |Název testu                               |      A        |
|stdin             |Co má jít do standardního vstupu programu |      A        |
|stdout            |Očekávaný výstup programu                 |      A        |
|popis             |Popis testu                               |      N        |
|spustitelny_soubor|Název programu                            |      A        |

Zde je příklad testu, který byl vytvořen přepsáním ukázkového vstupu ze zadání.
```json
{
    "jmeno" : "Test ze zadání",
    "stdin" : "Centralni, Brno_01, Brno_02, Praha, Ostrava, Export\nauto_01: Centralni > Brno_01 > Brno_02\nauto_02: Centralni > Ostrava > Centralni\nletadlo_01: Centralni > Export\nvlak_a: Praha > Centralni\nauto_03: Brno_01 > Brno_02",
    "stdout" : "nejvice navstevovany: Centralni 5\nexistuje vice spojeni: ano\nzbozi zpet do skladu:ano",
    "popis" : "Test, který je popsaný v zadání",
    "spustitelny_soubor" : "distribution"
}
```