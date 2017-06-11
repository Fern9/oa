def trans_up(string):
    if string == 'class':
        return 'className'
    ans = ''
    upper = False
    for i in xrange(len(string)):
        s = string[i]
        if s == '-':
            upper = True
        else:
            if upper:
                s = s.upper()
            ans += s
            upper = False

    return ans


with open('./a', 'r') as f:
    lines = f.readlines()
    events = []
    vars = []
    for line in lines:
        line = line.strip()
        if line.startswith('bind'):
            events.append(line)
        else:
            vars.append(line)

    for i, line in enumerate(vars):
        print '%s: {}%s' % (trans_up(line), '' if i == len(lines) - 1 else ',')

    print ' '
    print ' '
    for line in vars:
        print '%s="{{%s}}" ' % (line, trans_up(line)),

    for line in events:
        print '%s="%s" ' % (line, trans_up(line)),

    print ' '
    print ' '

    for i, line in enumerate(events):
        dh = '' if i == len(events) - 1 else ','
        evF=line[4:]
        out = u"{bindF}(...v) {{\nthis.$emit('{evF}', ...v)\n}}{dh}".format(dh=dh, evF=evF,bindF=line)
        print out
