#from status_codes import error500

def render(filename, context={}):
    print("rendering")
    html_str = ""
    with open(filename, 'r') as f:
        html_str = f.read()
        html_str = html_str.format(**context)
    return html_str