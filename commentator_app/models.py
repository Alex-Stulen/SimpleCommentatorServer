import mimetypes

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

from PIL import Image

from commentator_app.validators.files import FileValidator


class CommentManager(models.Manager):
    def all(self):
        return self.filter(is_published=True).select_related().order_by('-created_at')

    def all_main_comments(self):
        return self.all().filter(reply_to=None)

    def replies_all(self, instance):
        return self.filter(reply_to=instance.pk, is_published=True).select_related().order_by('-created_at')

    def replies_all_count(self, instance):
        return self.filter(reply_to=instance.pk, is_published=True).count()


class AbstractComment(models.Model):
    class Meta:
        abstract = True

    username_validator = UnicodeUsernameValidator()

    image_max_width = 320  # px
    image_max_height = 240  # px

    allowed_file_content_types = ('image/jpeg', 'image/gif', 'image/png', 'text/plain')
    # 1024 * 100 = 100kB
    file_validator = FileValidator(max_size=1024 * 100, content_types=allowed_file_content_types)

    objects = CommentManager()

    username = models.CharField(
        _('Username'),
        max_length=150,
        unique=False,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
    )

    email = models.EmailField(_('Email address'))
    home_page = models.URLField(_('Home page'), blank=True)
    text = models.TextField(_('Comment text'), max_length=2048)
    file = models.FileField(_('File'), blank=True,
                            upload_to='uploads/commentator/%Y/%m/%d', validators=[file_validator, ])
    is_published = models.BooleanField(_('Is published'), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(AbstractComment):
    reply_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE, default=None, blank=True)

    def is_image_file(self):
        if not self.file:
            return False

        try:
            file_type = mimetypes.guess_type(self.file.url)[0]
            if 'image' in file_type.lower():
                return True
        except IndexError:
            return False
        except Exception as e:
            return False

    def normalize_image_size(self):
        if not self.is_image_file():
            return

        img = Image.open(self.file.path)

        width_percent = (self.image_max_width / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percent)))

        new_image = img.resize((self.image_max_width, height_size))
        new_image.save(self.file.path)

    def get_image_size(self):
        if not self.file:
            return 0, 0
        return Image.open(self.file.path).size

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)

        if self.file and self.is_image_file() and self.get_image_size()[0] > self.image_max_width:
            self.normalize_image_size()

    def __str__(self):
        return f'id: {self.pk} -> {self.username}'
