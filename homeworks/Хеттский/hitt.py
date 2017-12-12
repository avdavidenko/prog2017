import sqlite3

gloss = {'1PL':'first person, plural',
         '2PL':'second person, plural',
         '3PL':'third person, plural',
         '1SG':'first person, singular',
         '2SG':'second person, singular',
         '3SG':'third person, singular',
         'ABL':'ablative case',
         'ACC':'accusative case',
         'ADJ':'adjective',
         'ADV':'adverb',
         'AUX':'auxiliary',
         'C':'common gender; complementizer',
         'COMP':'complementizer',
         'CONJ':'conjunction',
         'CONN':'connective',
         'DAT':'dative case',
         'DAT-LOC':'dative-locative case',
         'DEM':'demonstrative pronoun',
         'EMF':'emphatic',
         'EMPH':'emphatic',
         'ENCL':'enclitic',
         'ENLC':'UNKNOWN',
         'GEN':'genitive case',
         'IMF':'UNKNOWN',
         'IMP':'imperative mood',
         'IMPF':'imperfect',
         'INDEF':'indefinite pronoun',
         'INF':'infinitive',
         'INST':'instrumental case',
         'INSTR':'instrumental case',
         'LOC':'locative case',
         'MED':'medium',
         'N':'noun',
         'NEG':'negative',
         'NOM':'nominative case',
         'NUM':'cardinal',
         'P':'preposition (postposition)',
         'PART':'particle',
         'PERS':'personal',
         'POSS':'possessive pronoun',
         'PL':'plural',
         'PRON':'pronoun',
         'PRS':'present tense',
         'PRT':'preterite',
         'PRV':'preverb',
         'PST':'past tense',
         'PTCP':'participle',
         'REFL':'reflexive',
         'REL':'relative pronoun',
         'SG':'singular',
         'Q':'question word',
         'QUOT':'quotative',
         'V':'verb',
         'VOC':'vocative case'}

def only_glosses(mass_of_rows):
    pure_glosses = []
    all_glosses = []
    for row in mass_of_rows:
        glosses = row[2].split('.')
        for i in range (len (glosses)):
            if not glosses[i].isupper():
                glosses[i] = ''
            elif glosses[i] == 'I':
                glosses[i] = ''
        pure = ''
#        print(glosses)
        for i in range (len(glosses)):
            if glosses[i] != '':
                all_glosses.append(glosses[i])
                if pure != '':
                    pure = pure + '.' + glosses[i]
                else:
                    pure = glosses[i]
#        print(pure)
        pure_glosses.append(pure)
    gloss_dict = gloss_counter(all_glosses)
    gloss_table (gloss_dict)    
    return pure_glosses

def gloss_counter (all_glosses):
    gloss_dict = dict.fromkeys(all_glosses, 0)
    for a in all_glosses:
        gloss_dict[a] += 1
    graphs (gloss_dict)
    return gloss_dict

def gloss_table (gloss_dict):
    mass_of_gloss_rows = []
    for item in gloss_dict:
        a = []
        a.append (item)
        if item in gloss:
            a.append (gloss.get(item))
        else:
            a.append ('')
#        print (a)
        mass_of_gloss_rows.append (a)
    print (mass_of_gloss_rows)
#    c.execute('CREATE TABLE glosses(gloss text, meaning text)')
    for row in mass_of_gloss_rows:
        c.execute('INSERT INTO glosses VALUES(?,?)', row)
    return

def graphs (gloss_dict):
    X = []
    Y = []
    for item in gloss_dict:
        X.append(item)
        Y.append(gloss_dict.get(item))
#    print (X)
#    print (Y)
    return

def only_wordforms(mass_of_rows):
    pure_wordforms = []
    for row in mass_of_rows:
        a = row[1]
        pure_wordforms.append (a)
    return pure_wordforms

def only_lemmas(mass_of_rows):
    pure_lemmas = []
    for row in mass_of_rows:
        a = row[0]
        pure_lemmas.append (a)
    return pure_lemmas

def new_rows(mass_of_lemmas, mass_of_wordforms, mass_of_glosses):
    new_rows = []
    for i in range (len(mass_of_lemmas)):
        a = []
        a.append(mass_of_lemmas[i])
        a.append(mass_of_wordforms[i])
        a.append(mass_of_glosses[i])
        new_rows.append (a)        
    return new_rows

conn = sqlite3.connect('hittite.db')
c = conn.cursor()
#c.execute('CREATE TABLE words(lemma text, wordform text, glosses text)')
mass_of_rows = []
for row in c.execute('SELECT * FROM wordforms'):
    mass_of_rows.append(row)
#    print (row)
#    print (row)
#print(len(mass_of_rows))
mass_of_lemmas = only_lemmas(mass_of_rows)
mass_of_wordforms = only_wordforms (mass_of_rows)
mass_of_glosses = only_glosses(mass_of_rows)
mass_of_rows = new_rows(mass_of_lemmas, mass_of_wordforms, mass_of_glosses)
#print (mass_of_rows)
i = 0
for row in mass_of_rows:
    c.execute ('INSERT INTO words VALUES(?,?,?)', row)
    i = i+1
#c.execute('CREATE TABLE glosses(gloss text, meaning text)')
#for row in c.execute ('SELECT glosses
conn.commit()

