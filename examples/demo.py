
from buche import buche, H

# You don't have to set a template, but if you do, it must be the
# very first command you emit, before any printing.
# You can also give `src=<path-to-file>` instead of `content=...`
buche.command_template(content=H.div['my-template'](address="/"))

# Use this command to add styles, stylesheets, scripts, etc.
buche.command_resource(content=H.style(
    """
    .my-template {
        background-color: #eee;
        padding: 5px;
        display: flex;
        flex-direction: column;
        align-items: start;
    }
    """
))

# Display simple HTML
buche.html.h3('Welcome!')

# Display objects
buche(1234)
buche([x * x for x in range(100)])
buche.dict(avocado="green", banana="yellow", cherry="red")

# Open automatically creates an address for an element
div1 = buche.open.div(style="border: 3px solid red")

# You can also set an address explicitly
buche.html.div(address='/two', style="border: 3px solid blue")

# Get a printer for the given address
div2 = buche['/two']

# These objects will go in the divs
div1('One')
div2('Two')
div1('One again')

# Handy tabs component
grocery_list = buche.open.boxTabs()
fruit = grocery_list.open.tabEntry(
    label='Fruits',
    active=True,
)
vegetable = grocery_list.open.tabEntry(
    label='Veggies',
)

fruit.html.div(H.s("Pineapple"))
fruit.html.div("Raspberry")
fruit.html.div("Grape")

vegetable.html.div("Carrot")
vegetable.html.div("Potato")
vegetable.html.div("Yam")

# Customize the representation of a class
class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __hrepr__(self, H, hrepr):
        sz = hrepr.config.swatch_size or 20
        return H.div(
            style=f'display:inline-block;width:{sz}px;height:{sz}px;margin:2px;'
                f'background-color:rgb({self.r},{self.g},{self.b});'
        )

# This will call __hrepr__
buche(Color(255, 0, 0))

# Configuration values can be anything and are propagated recursively
buche(Color(0, 0, 255), swatch_size=50)

# You can evaluate JavaScript on elements
button = buche.open.button("Tickle me")
button.command_eval(expression="this.onclick = () => alert('Hihihihi!')")
