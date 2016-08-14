from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader('geotagger', 'templates'))
template = env.get_template('gpx.xml')


def generate_gpx(storylines):
    return template.render(storylines=storylines)

