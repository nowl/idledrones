from random import randint

prefixes = ['lo', 'tu', 'to', 'sm', 'aess', 'shun', 'eth', 'sma', 'ac', 'pla',
            'as', 'pra', 'plak', 'ithe', 'klu', 'ofen', 'ish', 'aing', 'clex', 'ush',
            'raish', 'it', 'daesh', 'ouff', 'kre', 'thi', 'er', 'ini', 'untuen', 'plol',
            'gem', 'sh', 'kel', 'on', 'un', 'no', 'sef', 'ro', 'kni',
            'h', 'dreb', 'eus', 'v', 'kn', 'ploeh', 'chet', 'sew', 'kr',
            'ean', 'eanon', 'thes', 'cl', 's', 'emn', 'ung', 'shauh', 'smaih', 'um',
            'uff', 'aack', 'iz', 'touck', 'ack', 'dr', 'ouc', 'umn']
suffixes = ['effola', 'ellaw', 'usse', 'ung', 'asa', 'ueck', 'uov', 'cell', 'ock', 'uova',
            'oort', 'toff', 'oeng', 'kest', 'osu', 'oune', 'aiheth', 'ire', 'emn', 'aev',
            'ir', 'oll', 'et', 'eze', 'art', 'aca', 'oost', 'eviv', 'aff', 'ert',
            'ne', 'oute', 'le', 'ent', 'oot', 'fe', 'urgu', 'eff', 'umne',
            'ete', 'acke', 'ooff', 'esest', 'ucka', 'eth', 'affu', 'airt', 'oe', 'est',
            'oneth', 'iemn', 'ese', 'auva', 'uss', 'unga', 'olle', 'uck',
            'iarart', 'oung', 'eng', 'ono', 'ena', 'egent', 'ala', 'acuff', 'arg']

def roman_num(num):
    if num < 1 or num > 10:
        return ''
    return {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
            6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X'}[num]

set_prefixes = set(prefixes)
set_suffixes = set(suffixes)

print len(set_prefixes), len(prefixes)
print len(set_suffixes), len(suffixes)

names = []
for i in range(1000):
    prefix = prefixes[randint(0, len(prefixes)-1)]
    suffix = suffixes[randint(0, len(suffixes)-1)]
    new_name = list(prefix + suffix)
    new_name[0] = new_name[0].upper()
    new_name.append(' ')
    new_name.append(roman_num(randint(1, 10)))
    new_name = ''.join(new_name)
    #if new_name not in names:
    names.append(new_name)

set_names = set(names)
print len(names), len(set_names)

print list(set_names)[0:10]
