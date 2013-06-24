def humanize(s):
    result = ''
    if s.isupper():
        result = s.lower()
    else:
        for c in s:
            if c.isupper():
                result = '%s %s' % (result.rstrip(), c.lower())
            else:
                result = '%s%s' % (result, c)
    result = result.strip()
    return result
