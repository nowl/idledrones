from random import randint

prefixes = ['lo', 'tu', 'to', 'sm', 'aess', 'shun', 'eth', 'sma', 'ac', 'pla',
            'as', 'pra', 'plak', 'ithe', 'klu', 'ofen', 'ish', 'aing', 'clex', 'ush',
            'raish', 'it', 'daesh', 'ouff', 'kre', 'thi', 'er', 'ini', 'untuen', 'plol',
            'gem', 'sh', 'kel', 'on', 'un', 'no', 'sef', 'ro', 'kni']
suffixes = ['effola', 'ellaw', 'usse', 'ung', 'asa', 'ueck', 'uov', 'cell', 'ock', 'uova',
            'oort', 'toff', 'oeng', 'kest', 'osu', 'oune', 'aiheth', 'ire', 'emn', 'aev',
            'ir', 'oll', 'et', 'eze', 'art', 'aca', 'oost', 'eviv', 'aff', 'ert',
            'ne', 'oute', 'le', 'ent', 'oot', 'fe', 'urgu', 'eff', 'umne']

'''
    Shete
    Hacke
    Drebooff
    Eusesest
    Vucka
    Kneth
    Ploehaffu
    Chetairt
    Sewoe
    Krest

    Eanoneth
    Thesiemn
    Clese
    Sert
    Eruoth
    Emnauva
    Unguss
    Shauhunga
    Smaiholle
    Umuck

    Uffiarart
    Asoung
    Aackete
    Izeng
    Smono
    Touckena
    Ackegent
    Drala
    Oucacuff
    Umnarg
'''

set_prefixes = set(prefixes)
set_suffixes = set(suffixes)

print len(set_prefixes), len(prefixes)
print len(set_suffixes), len(suffixes)

names = []
for i in range(50):
    prefix = prefixes[randint(0, len(prefixes)-1)]
    suffix = suffixes[randint(0, len(suffixes)-1)]
    names.append(prefix + suffix)

set_names = set(names)
print len(names), len(set_names)

print set_names

'''
add I, II, III, IV, etc.
'''
