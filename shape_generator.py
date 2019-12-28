import click


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    '--size', required=True, type=int,
    help='Number of generated images per each shape'
)
@click.option(
    '--destination', required=True, help='Storage path'
)
@click.option(
    '--show-animation', default=False,
    help="Shows turtle animation while generating, "
         "note if this option is activated it slows the generation process"
)
def generate_shapes(size, destination, show_animation):
    """
        Generate a defined number of images that contains eight geometric
        shapes (Square, Triangle, Circle, Star, Polygon, Pentagon, Heptagon,
        Hexagon).

        Each shape is drawn randomly on a 200x200 image. Each image is drawn
        with the following parameters which their value is selected randomly
        and independently :

            - Image's background color
            - Shape's filling color
            - Shape's rotation angle (between -180° and 180°)
            - Center of the circumscribed circle of a shape

    """
    from generator import GeometricShapes
    generator = GeometricShapes(
        size=size, destination=destination, animation=show_animation
    )
    generator.generate()


if __name__ == '__main__':
    cli()
