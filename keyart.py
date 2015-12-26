import sys
def draw_art(key_size, key_algo, key_fpr):
    """Execute the Drunken Bishop algorithm on a key."""
    art = ''
    f_bytes = []
    pos = 104
    walk = [pos]
    visits = [0]*209
    temp = ''

    try:
        key_bin = bin(int(key_fpr, 16))[2:].zfill(len(key_fpr)*4)
    except ValueError:
        print("The supplied fingerprint is not a hexadecimal string.")
        sys.exit(3)

    for i, char in enumerate(key_bin):
        temp += char
        if i % 2 == 1:
            f_bytes.append(temp)
            temp = ''

    # create a little-endian bit-pair array
    for i in range(0, len(f_bytes), 4):
        f_bytes[i], f_bytes[i+3] = f_bytes[i+3], f_bytes[i]
        f_bytes[i+1], f_bytes[i+2] = f_bytes[i+2], f_bytes[i+1]

    for pair in f_bytes:
        if (20 <= pos <= 36 or 39 <= pos <= 55 or 58 <= pos <= 74 or
                77 <= pos <= 93 or 96 <= pos <= 112 or 115 <= pos <= 131 or
                134 <= pos <= 150 or 153 <= pos <= 169 or 172 <= pos <= 188):
            if   pair == '00':
                pos -= 20 # Square 'M'
            elif pair == '01':
                pos -= 18
            elif pair == '10':
                pos += 18
            else:
                pos += 20
        elif 1 <= pos <= 17: # Square 'T'
            if pair == '00':
                pos -= 1
            elif pair == '01':
                pos += 1
            elif pair == '10':
                pos += 18
            else:
                pos += 20
        elif 191 <= pos <= 207: # Square 'B'
            if pair == '00':
                pos -= 20
            elif pair == '01':
                pos -= 18
            elif pair == '10':
                pos -= 1
            else:
                pos += 1
        elif pos in [19, 38, 57, 76, 95, 114, 133, 152, 171]: # Square 'L'
            if pair == '00':
                pos -= 19
            elif pair == '01':
                pos -= 18
            elif pair == '10':
                pos += 19
            else:
                pos += 20
        elif pos in [37, 56, 75, 94, 113, 132, 151, 170, 189]: # Square 'R'
            if pair == '00':
                pos -= 20
            elif pair == '01':
                pos -= 19
            elif pair == '10':
                pos += 18
            else:
                pos += 19
        elif pos == 0: # Square 'a'
            if pair == '01':
                pos += 1
            elif pair == '10':
                pos += 19
            elif pair == '11':
                pos += 20
        elif pos == 18: # Square 'b'
            if pair == '00':
                pos -= 1
            elif pair == '10':
                pos += 18
            elif pair == '11':
                pos += 19
        elif pos == 190: # Square 'c'
            if pair == '00':
                pos -= 19
            elif pair == '01':
                pos -= 18
            elif pair == '11':
                pos += 1
        else: # Square 'd'
            if pair == '00':
                pos -= 20
            elif pair == '01':
                pos -= 19
            elif pair == '10':
                pos -= 1
        walk.append(pos)

    for square in walk:
        visits[square] += 1
        if visits[square] > 18:
            visits[square] = 18

    # See https://tools.ietf.org/html/rfc4880#section-9.1
    # Also https://tools.ietf.org/html/rfc6637#section4
    if key_algo == '17':
        key_algo = 'DSA'
    elif key_algo == '1' or key_algo == '2' or key_algo == '3':
        key_algo = 'RSA'
    elif key_algo == '16' or key_algo == '20':
        key_algo = 'Elg'
    elif key_algo == '18':
        key_algo = 'ECDH'
    elif key_algo == '19':
        key_algo = 'ECDSA'
    elif key_algo == '21':
        key_algo = 'X9.42'
    else:
        key_algo = 'N/A'

    if key_size:
        header = "["+key_algo+" "+key_size+"]"
    else:
        header = ''

    if len(header) > 19:
        header = ''
    art += '+' + header.center(19, '-') + '+\n'

    for i, visit in enumerate(visits):
        # Build up the art with the boundaries and newlines
        if i % 19 == 0:
            art += "|{}"
        elif i % 19 == 18:
            art += "{}|\n"
        else:
            art += '{}'

        # Insert the 'coin' into the art at this position
        if i == 104: # Starting position
            art = art.format(_get_coin(visit, coin='S'))
        elif i == walk[len(walk)-1]: # Ending position
            art = art.format(_get_coin(visit, coin='E'))
        else:
            art = art.format(_get_coin(visit, ansi_art=True))

    if key_size:
        footer = "["+key_fpr[-16:]+"]"
    elif key_size:
        footer = "["+key_fpr[-8:]+"]"
    else:
        footer = ''

    art += '+' + footer.center(19, '-') + '+'

    return art

def _get_coin(num_of_hits, ansi_art=False, coin=None):
    """Returns the coin for this humber of hits. If ansi_art is enabled the coin
    will be colorized with ansi codes. If coin is not None, it will use that
    coin instead of the default (used for the 'S' and 'E', start end coins)."""
    coins = [' ', '.', '^', ':', 'l', 'i', '?', '(', 'f', 'x', 'X', 'Z', '#',
             'M', 'W', '&', '8', '%', '@']
    colors = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
              '', '', '']
    reset = ''
    if ansi_art:
        colors = [
            '', # no coin
            '\033[38;5;21m', # blue (cold)
            '\033[38;5;39m',
            '\033[38;5;50m',
            '\033[38;5;48m',
            '\033[38;5;46m', # green
            '\033[38;5;118m',
            '\033[38;5;190m',
            '\033[38;5;226m', # yellow
            '\033[38;5;220m',
            '\033[38;5;214m', # orange
            '\033[38;5;208m',
            '\033[38;5;202m',
            '\033[38;5;196m', # red
            '\033[38;5;203m',
            '\033[38;5;210m',
            '\033[38;5;217m', # pink
            '\033[38;5;224m',
            '\033[38;5;231m'  # white (hot)
        ]
        reset = '\033[0m'

    color = colors[num_of_hits]
    if not coin:
        coin = coins[num_of_hits]
    return '{}{}{}'.format(color, coin, reset)
