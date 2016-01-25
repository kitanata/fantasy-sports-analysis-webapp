from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks


class HomePage(Page):
    body = StreamField([
        ('text', blocks.CharBlock()),
        ('paragraph', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]

    parent_page_types = []
