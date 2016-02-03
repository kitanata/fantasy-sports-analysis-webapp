from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock


class JumbotronBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True)
    body = blocks.RichTextBlock()
    image = ImageChooserBlock()

    class Meta:
        icon = 'image'
        template = 'home/blocks/_jumbotron_block.html'
