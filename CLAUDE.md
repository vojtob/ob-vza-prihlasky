# Popisy pretekov pre prihlasovací systém VZA

Repozitár slúži na prípravu popisov pretekov v orientačnom behu pre interný prihlasovací systém klubu
Slávia ŽU Žilina (VZA). Popis je HTML fragment, ktorý Vojto ručne nakopíruje do žltej časti „Pokyny"
pri preteku na https://www.vza.sk/treningy/index.php.

## Záväzné pravidlá

1. **Najprv plán, potom vykonanie.** Pri každej akcii (aj pri každom príkaze `/ob-pretek`, `/ob-kalendar`,
   `/ob-kontrola`) najprv zisti podklady a popíš, čo ideš urobiť: ktoré súbory vzniknú alebo sa zmenia,
   z akých údajov, a čo je neisté. Súbory v repozitári zapisuj až po výslovnom schválení.
   Bez schválenia smieš len čítať a sťahovať podklady do scratchpadu.
2. **Nikdy nič nezapisuj na vza.sk ani na is.orienteering.sk.** Žiadne prihlasovanie, odosielanie
   formulárov, požiadavky meniace údaje, ani cez prehliadačové nástroje. Z oboch stránok sa iba číta.
   Výsledok vždy kopíruje Vojto ručne.
3. Necommituj bez požiadania.
4. Nič nedomýšľaj. Čo nie je v IS ani v propozíciách, do popisu nedávaj a uveď to v zhrnutí.

## Zdroje údajov

| Čo | Kde |
|---|---|
| Kalendár pretekov | https://is.orienteering.sk/competitions (odkazy `/competitions/<ID>`) |
| Stránka pretekov | `https://is.orienteering.sk/competitions/<ID>` – názov, dátum, miesto, klasifikácia, etapy (dátum + disciplína), „Dátumy prihlášok", „Ceny prihlášok" (zoznam kategórií), „Dokumenty" |
| Propozície | odkaz „Propozície" v časti Dokumenty, zvyčajne `…/competition_documents/<rok>/<mesiac>/<ID>/<ID>_invitation_sk.pdf` |
| Čo je už vo VZA | https://www.vza.sk/treningy/index.php (zoznam) a `pretek.php?id=<N>` (aktuálne vložené Pokyny) |

Všetko je čitateľné bez prihlásenia. Stránky sťahuj cez `curl -sS -m 30 -o <súbor> <url>` do
scratchpadu (nie do repozitára), PDF čítaj cez `pdftotext -layout <súbor> -`; ak je PDF sken a text
je prázdny, otvor ho nástrojom Read. Filter kalendára v IS je POST formulár – nepoužívaj ho, stačí
predvolený zoznam najbližších pretekov.

## Štruktúra repozitára

- `templates/` – šablóny popisov (SRJ, majstrovstvá, majstrovstvá štafiet, stredoliga)
- `preteky/RRRR-MM-DD Miesto/` – jeden priečinok na podujatie (dátum 1. etapy), v ňom popisy a exporty prihlásených (`zoznam*.csv`, `*.xlsx` – tie nevytváraj ani neupravuj)
- `preteky/Archive/` – staré podujatia
- `ob_convert.py` – prevod exportu prihlásených, s popismi nesúvisí

## Postup prípravy pretekov

1. Nájdi ID pretekov (dostaneš ID, URL, alebo názov/dátum – vtedy hľadaj v kalendári).
2. Stiahni stránku pretekov a propozície.
3. Urči typ (klasifikácia) a etapy. **Každá etapa = samostatný súbor** (obmedzenie systému VZA).
4. Vyber šablónu a vyplň ju podľa pravidiel nižšie.
5. Prejdi kontrolný zoznam.
6. Predlož návrh (obsah súborov + zhrnutie) a po schválení súbory zapíš.

### Výber šablóny

| Klasifikácia v IS | Šablóna |
|---|---|
| Slovenský rebríček | `templates/template_SRJ.html` |
| Majstrovstvá Slovenska (jednotlivci) | `templates/template_majstrovstva.html` |
| Majstrovstvá Slovenska štafiet | `templates/template_majstrovstva_stafety.html` |
| Oblastný rebríček – oblasť STRED (Stredoliga) | `templates/template_stredoliga.html` |
| Iné (O-Cup, viacdňové verejné preteky…) | vychádzaj z SRJ, jeden blok „Kategórie" |

Ak má podujatie etapy rôzneho typu (napr. sobota MSR, nedeľa SRJ), každá etapa použije svoju šablónu.

### Pravidlá pre jednotlivé časti

**Nadpis `<H1>`** – typ + disciplína etapy:
- SRJ: „Slovenský rebríček jednotlivcov na stredných tratiach" / „na dlhých tratiach" / „v šprinte"
- MSR: „Majstrovstvá Slovenska v OB na strednej trati" / „na dlhej trati" / „v šprinte" / „Majstrovstvá Slovenska v nočnom OB" / „Majstrovstvá Slovenska štafiet"
- Stredoliga: „Stredoliga"
- Iné: názov podujatia z IS

**Podnadpis** (0–3 riadky pod H1, každý ukončený `<BR>`) – z propozícií: názov podujatia, memoriál,
pohár, ročník, „World Ranking Event". Pri Stredolige jeden riadok:
„Preteky v orientačnom behu STREDOLIGA RRRR – N. kolo Miesto".

**Dátum** – dátum etapy z IS vo formáte `D.M.RRRR (deň)` bez úvodných núl, napr. `17.10.2026 (sobota)`.
Ak propozície uvádzajú čas štartu 00, pridaj ` o HH:MM`. Deň v týždni vždy vypočítaj (`date -d`).

**Miesto** – centrum pretekov z propozícií; obec tučným (`<b>`), za ňou medzera a popis centra,
na konci odkaz `(mapa)`:
- ak propozície obsahujú odkaz na mapu, použi ho;
- ak obsahujú GPS súradnice, použi `https://mapy.com/fnc/v1/showmap?mapset=outdoor&center=<lon>,<lat>&zoom=16&marker=true`;
- inak odkaz vynechaj a uveď to v zhrnutí. Polohu nehádaj.

**Popis** – odkaz na `https://is.orienteering.sk/competitions/<ID>`, rovnaký pre všetky etapy.

**Kategórie**
- Zoznam ber z časti „Ceny prihlášok" v IS (je úplný) a over ho oproti propozíciám; rozdiely uveď v zhrnutí.
- Zápis skrátene, jeden riadok na pohlavie, najprv W, potom M, vekovo vzostupne:
  `W 12A, 14A, 16A, …` / `M 12A, 14A, 16A, …`
- Bloky podľa propozícií: „Kategórie - SRJ", „Kategórie - Majstrovstvá SR", „Kategórie - Verejné preteky".
- Verejné: `W10, M10`, `MWR - deti so sprievodom`, `K - kondičná, orientačne náročná trať`,
  `N - náborová trať pre začiatočníkov`; ak propozície uvádzajú dĺžku trate, pridaj ju
  (napr. „v dĺžke cca 3 km"). Ďalšie verejné kategórie (W10S/M10S, Open…) len ak sú v propozíciách.
- Ak sa kategórie medzi etapami líšia, každý súbor má svoje.

**Stredoliga**
- Kategórie sú trate A/B/C: náročnosť, dĺžka (príp. prevýšenie a počet kontrol) a vekové kategórie podľa propozícií; osobitnú formu (scorelauf, voľné poradie kontrol) uveď.
- Blok „Platba": ceny podľa trate z propozícií a vždy tieto dva riadky s IBAN-om z propozícií:
  - `Deťom sa štartovné preplatí, za tie neplaťte`
  - `<b>Dospelí si uhradia za seba štartovné na účet: IBAN …</b>`

**Štafety** – ponechaj záverečný odsek šablóny o zápise štafety do poznámky (`VZA 1-1`, `VZA 1-2`…).

### Pomenovanie súborov

`preteky/RRRR-MM-DD Miesto/RRRR-MM-DD_<typ>_<disciplina>.html`, napr.
`preteky/2026-10-17 Ladomerska Vieska/2026-10-17_SRJ_long.html` a `2026-10-18_SRJ_middle.html`.
Typ: `SRJ`, `MSR`, `stredoliga`, inak krátky názov. Disciplína: `sprint`, `middle`, `long`, `night`,
`stafety`. Názvy bez diakritiky. Existujúce staršie súbory nepremenúvaj.

### Kontrolný zoznam

- dátum a rok sedia s etapou v IS, deň v týždni je vypočítaný
- ID v odkaze „Popis" je správne
- nič nezostalo zo šablóny (starý dátum, miesto, mapa, podnadpis, kategórie, komentár)
- všetky značky sú uzavreté; súbor je fragment bez `<html>`/`<body>`, v UTF-8
- pri viacdňových pretekoch je miesto, mapa a odkaz rovnaký vo všetkých súboroch

### Zhrnutie pre Vojta

Po príprave vypíš pre každú etapu údaje do formulára VZA:

- **Názov:** napr. „SRJ Dlhá trať, Ladomerská Vieska", „Stredoliga Vrútky"
- **Dátum konania:** `DD-MM-RRRR HH:MM`
- **Prihlasovanie do:** deň pred uzávierkou prihlášok v IS o 19:00 (uveď aj samotnú uzávierku v IS)
- **Súbor:** cesta k HTML

A zoznam vecí, ktoré sa nedali overiť alebo sa líšia medzi IS a propozíciami.
