from wagtail.core.models import Page,Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel,InlinePanel,MultiFieldPanel,FieldRowPanel
from django.db import models
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from .blocks import TwoColumnBlock
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from django.db import models


from modelcluster.models import ClusterableModel

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from django_extensions.db.fields import AutoSlugField


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

#class AboutUs(Page):
    #intro = RichTextField(blank=True)
    #search_fields = Page.search_fields + [
#   index.SearchField('intro'),
#]
#   content_panels = Page.content_panels + [

#       FieldPanel('intro', classname="full"),
#       InlinePanel('gallery_images', label="Gallery images"),

   # ]

class AboutUs(Page):
    template="home/about_us.html "
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('intro', blocks.RichTextBlock()),
        ('two_columns', TwoColumnBlock()),
        ('image', ImageChooserBlock(icon="image")),

    ],null=True,blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]





#class AboutUsGalleryImage(Orderable):
   # page = ParentalKey(AboutUs, on_delete=models.CASCADE, related_name='gallery_images')
    #image = models.ForeignKey(
    #    'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
   # )
   # caption = models.CharField(blank=True, max_length=250)

  #  panels = [
     #   ImageChooserPanel('image'),
     #   FieldPanel('caption'),
    #]

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='custom_form_fields')

class FormPage(AbstractEmailForm):
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('custom_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email Notification Config"),
    ]

    def get_form_fields(self):
        return self.custom_form_fields.all()


class MenuItem(Orderable):

    link_title = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )
    link_url = models.CharField(
        max_length=500,
        blank=True
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return 'Missing Title'


@register_snippet
class Menu(ClusterableModel):
    """The main menu clusterable model."""

    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True)
    # slug = models.SlugField()

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
        ], heading="Menu"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title

class TextPage(Page):
    text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('text', classname='full'),
    ]