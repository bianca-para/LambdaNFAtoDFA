def transf_sir(set):
    elements = sorted(list(set))
    result = "{" + ",".join(map(str, elements)) + "}"
    return result

with open("lfa1.txt", "r") as f, open("lfa2.txt", "w") as g:
    nr_stari = int(f.readline().strip())
    stari = list(map(int, f.readline().split()))

    nr_litere = int(f.readline().strip())
    litere = f.readline().split()

    stare_initiala = int(f.readline().strip())

    nr_stari_finale = int(f.readline().strip())
    finale = set(map(int, f.readline().split()))

    num_tranzitii = int(f.readline().strip())

    tranzitii = {}

    for _ in range(num_tranzitii):
        mainKey, litera, smallKey = f.readline().split()
        mainKey = int(mainKey)
        smallKey = int(smallKey)
        if mainKey not in tranzitii:
            tranzitii[mainKey] = {}
        if litera not in tranzitii[mainKey]:
            tranzitii[mainKey][litera] = set()
        tranzitii[mainKey][litera].add(smallKey)


    for mainKey in stari:
        if mainKey not in tranzitii:
            tranzitii[mainKey] = {}

    dfa_mapare_stari = {}
    dfa_tranzitii = {}
    dfa_stari_finale = set()
    coada_stari = []

    set_initial_stari = {stare_initiala}
    coada_stari.append(set_initial_stari)
    dfa_contor_stari = 1
    dfa_mapare_stari[transf_sir(set_initial_stari)] = dfa_contor_stari

    if any(mainKey in set_initial_stari for mainKey in finale):
        dfa_stari_finale.add(dfa_contor_stari)

    ls=[]
    while coada_stari:
        current_set = coada_stari.pop(0)
        current_state = dfa_mapare_stari[transf_sir(current_set)]
        ls.append(current_set)
        dfa_tranzitii[current_state] = {}

        for litera in litere:
            new_set = set()
            for mainKey in current_set:
                if litera in tranzitii[mainKey]:
                    new_set.update(tranzitii[mainKey][litera])

            if not new_set:
                continue

            new_set_string = transf_sir(new_set)
            if new_set_string not in dfa_mapare_stari:
                dfa_contor_stari += 1
                dfa_mapare_stari[new_set_string] = dfa_contor_stari
                coada_stari.append(new_set)

                if any(mainKey in new_set for mainKey in finale):
                    dfa_stari_finale.add(dfa_contor_stari)

            dfa_tranzitii[current_state][litera] = dfa_mapare_stari[new_set_string]

    ls=sorted(ls,key=lambda x:len(x))
    for i in ls:
        print (sorted(i))
    g.write(str(dfa_contor_stari) + "\n")
    g.write(" ".join(map(str, range(1, dfa_contor_stari + 1))) + "\n")
    g.write(str(nr_litere) + "\n")
    g.write(" ".join(litere) + "\n")
    g.write("1\n")
    g.write(str(len(dfa_stari_finale)) + "\n")
    g.write(" ".join(map(str, dfa_stari_finale)) + "\n")

    numar_tranzitii = sum(len(transitions) for transitions in dfa_tranzitii.values())
    g.write(str(numar_tranzitii) + "\n")
    for mainKey, transitions in dfa_tranzitii.items():
        for litera, smallKey in transitions.items():
            g.write(f"{mainKey} {litera} {smallKey}\n")
