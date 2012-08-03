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

MAX_ROMAN_NUM = 20

def roman_num(num):
    if num < 1 or num > MAX_ROMAN_NUM:
        return ''
    return {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
            6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X',
            11: 'XI', 12: 'XII', 13: 'XIII', 14: 'XIV', 15: 'XV',
            16: 'XVI', 17: 'XVII', 18: 'XVIII', 19: 'XIX', 20: 'XX'}[num]

def get_name(existing_names = None):
    for i in range(25):
        prefix = prefixes[randint(0, len(prefixes)-1)]
        suffix = suffixes[randint(0, len(suffixes)-1)]
        new_name = list(prefix + suffix)
        new_name[0] = new_name[0].upper()
        new_name.append(' ')
        new_name.append(roman_num(randint(1, MAX_ROMAN_NUM)))
        new_name = ''.join(new_name)
        if not existing_names or (existing_names and new_name not in existing_names):
            return new_name
    return None
