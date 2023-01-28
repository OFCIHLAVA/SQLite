SQL UPDATE 26.1.2023

- databaze nastroje prehozena do SQL.

vytvorena databaze "programy" se tremi tabulkami.

+ tabilka dilu v databazi (vsechny poddily, ktere se nachazeji v databazi)
+ tabulka dilu a v jakych vsech monumentech se nachazeji
+ tabulka monumentu a jejich programu, pripadne specialnich pravidel.

seznam scriptu:
• unikatni dily v databazi - pripoji se na databazi programy, do tabulku dily v databazi 
a vybere vsechny unikatni dily z tabulky. Vysledek zapise do txt/ souboru ve slozce skriptu.

• 1_sqllite_boudaXprogram - skript na vytvoreni tabulky monumentu a jejich programu v databazi. Vezme data x txt souboru a vyrvori z nich tabulku.
• 2_dily_v_databazi - stejne jako vyse ale pro jednotlive dily v z kusovniku.
• 3_sqllite_dilyXboudy - stejne jako vyse ale pro kombinaci dil - v monumentu. Pro vsechny dily v kusovniku.

Modules
• queries - sql dotazy na ziskavani dat z databaze a nasledne promitnuti do Front endu
• sqllite - pracovni modul sql funkci pouyikvanych na vytvoreni a spravu slqllite databaze


TO DO:

Vyresit spravu databaze pres Front end.

• Udelat dalsi okno pro zobrazovani infa o tabulkach.
• Kontrola pritomnosti dilu a monumentu.
• sprava dilu a monumentu (add, update, delete)

• udelat nastroj na hromadny update kusovniku (napojist na stavajici updata - vyjet bomy  a podle nich aktualizovat databazi]
• udelat nastrnj na hromadnu update monumentu (nacucnout txt/xls a podle nej aktualiovat databazi]



