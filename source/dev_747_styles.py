HEX_COLORS_BOOTSTRAP = {
    'text': '#dbdbdb',
    'background': '#222',
    'gray': '#999',
    'gray-light': '#c1c1c1',
    'gray-light1': '#adb5bd',
    'gray-secondary': '#444',
    'gray-dark': '#303030',
    'gray-dark2': '#2b2a2a',
    'gray-dark2-border': '#242424',
    'blue-gray-dark': '#2a4663',
    'blue-gray-dark-border': '#28415b',
    'blue-dark': '#375a7f',
    'indigo': '#6610f2',
    'purple': '#6f42c1',
    'pink': '#e83e8c',
    'red': '#E74C3C',
    'orange': '#fd7e14',
    'yellow': '#F39C12',
    'green': '#00bc8c',
    'teal': '#20c997',
    'cyan': '#3498DB',
    'white': '#fff',
    'green-success': '#00bc8c',
    'blue-info': '#3498DB',
    'orange-warning': '#F39C12',
    'red-danger': '#E74C3C',
}

HEX_COLORS_CHART = {
    'Maroon': '#800000',
    'Brown': '#9A6324',
    'Olive': '#808000',
    'Teal': '#469990',
    'Navy': '#000075',
    'Black': '#000000',
    'Red': '#e6194B',
    'Orange': '#f58231',
    'Yellow': '#ffe119',
    'Lime': '#bfef45',
    'Green': '#3cb44b',
    'Cyan': '#42d4f4',
    'Blue': '#4363d8',
    'Purple': '#911eb4',
    'Magenta': '#f032e6',
    'Grey': '#a9a9a9',
    'Pink': '#fabebe',
    'Apricot': '#ffd8b1',
    'Beige': '#fffac8',
    'Mint': '#aaffc3',
    'Lavender': '#e6beff',
    'White': '#ffffff',
}

# return RGBA colors 
def selectHEXColor(color):
    if(color == 'color_muted_blue'):
        return ('#1f77b4')
    elif(color == 'safety_orange'):
        return ('#ff7f0e')
    elif(color == 'grey_header'):
        return ('#5a6777')
    elif(color == 'text_grey'):
        return ('#5a6777')
    elif(color == 'bgcolor'):
        return ('#1a1a1a')
    elif(color == 'graycolorarea'):
        return ('#333333')
    elif(color == 'graycolorarealight'):
        return ('#474747')
    elif(color == 'graycolorgrid'):
        return ('#2b2b2b')
    elif(color == 'textcolormain'):
        return ('#bababa')                
    else:
        return ('#1f77b4')
                
# return RGBA colors 
def selectRGBAcolor(color):
    if(color == 'color_red_07'):
        return ('rgba(184,46,46, 0.7)')
    elif(color == 'color_red1'):
        return ('rgba(184,46,46, 1)')
    elif(color == 'color_green07'):
        return ('rgba(102,170,0, 0.7)')
    elif(color == 'color_green1'):
        return ('rgba(102,170,0, 1)')
    elif(color == 'color_blue1'):
        return ('rgba(0,153,198, 1)')
    elif(color == 'color_orange1'):
        return ('rgba(230,115,0, 1)')
    else:
        return ('rgba(184,46,46, 0.7)')                