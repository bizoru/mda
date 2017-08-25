"""
An example how to generate angularjs code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""
from os import mkdir
from os.path import exists, dirname, join
import jinja2
from entity_test import get_entity_mm


def main(debug=False):

    this_folder = dirname(__file__)

    entity_mm = get_entity_mm(debug)

    # Build Person model from person.ent file
    person_model = entity_mm.model_from_file(join(this_folder, 'voto.ent'))


    # Create output folder
    srcgen_folder_controler = join(this_folder, 'srcgen/controllers')
    if not exists(srcgen_folder_controler):
        mkdir(srcgen_folder_controler)
    srcgen_folder_model = join(this_folder, 'srcgen/models')
    if not exists(srcgen_folder_model):
        mkdir(srcgen_folder_model)

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    # Register filter for mapping Entity type names to Java type names.
    #jinja_env.filters['javatype'] = javatype

    # Load template
    template = jinja_env.get_template('controler.template')

    for entity in person_model.entities:
        # For each entity generate java file
        with open(join(srcgen_folder_controler,
                       "%s.go" % entity.name.capitalize()), 'w') as f:
            f.write(template.render(entity=entity))

    # Load template
    template = jinja_env.get_template('model.template')

    for entity in person_model.entities:
        # For each entity generate java file
        with open(join(srcgen_folder_model,
                       "%s.go" % entity.name.capitalize()), 'w') as f:
            f.write(template.render(entity=entity))


if __name__ == "__main__":
    main()
