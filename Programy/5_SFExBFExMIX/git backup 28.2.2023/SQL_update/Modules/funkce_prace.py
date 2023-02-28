def import_kusovniku_LN(file):
    with open(file) as file:
        # Nacucne kusovnik z importu z LN a rozdeli jednotlive linky podle mezer na list listu(s jednotlivymi pn)
        linky_kusovniku = file.readlines()
        file.close()
        slinky_kusovniku = []
        for line in linky_kusovniku:
            if line[0] == "|":
                line = line.replace("|", "")
                sline = line.split()
                if len(sline) != 0:
                    slinky_kusovniku.append(sline)
        return(slinky_kusovniku)

def seznam_boud_z_importu(slinka_kusovniku):  # 1) Projet vsechny radky a ziskat seznam unikatnich vrcholu.
    unikatni_vrcholy = []
    for line in slinka_kusovniku:
        if line[0] not in unikatni_vrcholy:
            unikatni_vrcholy.append(line[0])
    return (unikatni_vrcholy)

def boudy_s_kusovnikem(unikatni_vrcholy, slinka_kusovniku):  # 2) Pro kazdy jeden vrchol projit vsechny linky a vytvorit list unikatnich PN pod tim vrcholem. Kazdy takovy list pak ulozi jako kvp vsech vrcholu(key) s jejich poddily(values).
    seznam_vrcholu = []
    seznam_vseho = {}
    for vrchol in unikatni_vrcholy:
        for line in slinka_kusovniku:
            if vrchol == line[0]:
                for pn in line:
                    if pn not in seznam_vrcholu:
                        seznam_vrcholu.append(pn)
        seznam_vseho[vrchol] = seznam_vrcholu  # Prida vrchol s unikatnimi pn do kvp vsech vrcholu(key) s jejich poddily(values).
        seznam_vrcholu = []
    # print(f'DICT databaze kusovniku: {seznam_vseho}')
    seznam_vseho_str = str(seznam_vseho)
    na_linky = seznam_vseho_str.replace("], ", "<+++>")
    rozdeleni_pn = na_linky.replace("', '", "|")
    apostrof = rozdeleni_pn.replace("'", "")
    leva_hranata = apostrof.replace("[", "")
    prava_hranata = leva_hranata.replace("]", "")
    mezera = prava_hranata.replace(" ", "")
    leva_slozena = mezera.replace("{", "")
    prava_slozena = leva_slozena.replace("}", "")
    str_dict_seznam_vseho = prava_slozena
    return seznam_vseho, str_dict_seznam_vseho

def nacteni_databaze_boud_pro_dotaz(file): #Nacucne vsechny boudy s jejich kusovniky ze soburu outputu z predchoziho kroku a pripravi je jako kvp pro dotazovani.
    with open(file) as file:
        data = file.readlines()
        file.close()
        boudy_kvp = {}
        data_all = []
        for part_data in data:
          part_data = part_data.replace("\n","")
          data_na_linky = part_data.split("<+++>")
          for kvp in data_na_linky:
            if kvp not in data_all:
              data_all.append(kvp)
        # print("pocet boud "+ str(len(data_all)))
        for line in data_all:
          bouda = line.split(":")[0]
          #print(bouda)
          items = line.split(":")[1].split("|")
          #print(items)
          #print(type(items))
          boudy_kvp[bouda] = items
    return(boudy_kvp)

def programy_boud(file):  # 3a) nacucnuti txt boud a programu a rozdeleni ze string na kvp.
    with open(file) as file:
        databaze_programu = file.readline().split(",")
        file.close()
        kvp_programy = {}
        # print(len(databaze_programu))
        for dvojice in databaze_programu:
            # print(dvojice)
            sdvojice = dvojice.split(":")
            kvp_programy[sdvojice[0]] = sdvojice[1]
    return (kvp_programy)

def dotaz_pn_program(pn, databaze, programy):  # 3b) Projde kusovnik vsech bud a kdyz je pn v kusovniku boudy, vrati jeji program
    vysledne_programy = []  # Vysledna kombinace programu.
    obsazeno_v_boudach = []
    dotaz = str(pn)
    #print("dotaz na PN: " + dotaz)
    for vrchol, pn_list in databaze.items():
        if dotaz in pn_list:
            program = programy.get(vrchol)
            obsazeno_v_boudach.append(f'{vrchol}({program})')
            if program not in vysledne_programy and program != None:
                vysledne_programy.append(program)
            #print(vrchol)
            #print(program)

    # A) Zjisteni vysledne SG z kombinace programu.  
    print(vysledne_programy)
    sfe = False
    bfe = False
    mix = False
    
    for program in vysledne_programy:
        print(program)
        if "SFE" in program:
            sfe = True
        if "BFE" in program:
            bfe = True
        if "MIX" in program:
            mix = True
    # B) Doplnkove zjisteni, jestli to je "specialni" polozka.  
    specialni_polozky = ""
    for program in vysledne_programy:
        if "AFDAL" in program:
            specialni_polozky += "(AFDAL)"
        if "AB MILITARI" in program:
            specialni_polozky += "(AB MILITARI)"
        if "DELTA LDMCR" in program:
            specialni_polozky += "(DELTA LDMCR)"
        if "VSB" in program:
            specialni_polozky += "(VSB)"

    # Vysledek

    # MIX polozky
    if mix or (bfe and sfe):    
        return [f'{dotaz}:MIX{specialni_polozky}', obsazeno_v_boudach] 
    # BFE polozky
    elif bfe and not sfe:
        return [f'{dotaz}:BFE{specialni_polozky}', obsazeno_v_boudach]
    # SFE polozky
    elif sfe and not bfe:
        return [f'{dotaz}:SFE{specialni_polozky}', obsazeno_v_boudach]
    # Nezname polozky
    else:
        # print(dotaz + "--- U tohoto pn neumim urcit - bud neznam toto pn, nebo nemam v databazi boudu, ve ktere je. Sorry :-( \n")
        return [f'{dotaz}:N/A', obsazeno_v_boudach]
    