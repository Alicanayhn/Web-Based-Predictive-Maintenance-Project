def take_theme(theme):
    if theme == 'orange':
        firstColor = '#F4CD00'
        secondColor = ['#F55600','#F45C01','#FF8900','#F5A600','#F5DC01','#F5F200']
        thirdColor = '#FF8900'

    elif theme == 'blue':
        firstColor = '#0001F5'
        secondColor = ['#230085','#0001F5','#0137FF','#0066FF','#01BCFA','#00CEF5']
        thirdColor = '#0137FF'
    
    else:
        firstColor = '#FF0083'
        secondColor = ['#FF0035','#F50076','#FF01AE','#F500ED','#E100FF','#BC00FA']
        thirdColor = '#F50076'

    return firstColor,secondColor,thirdColor