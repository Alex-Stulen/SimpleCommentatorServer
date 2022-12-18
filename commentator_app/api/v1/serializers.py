import mimetypes

from rest_framework import serializers

from drf_recaptcha.fields import ReCaptchaV2Field

from commentator_app import models


class CommentSerializer(serializers.ModelSerializer):
    recaptcha = ReCaptchaV2Field()

    class Meta:
        model = models.Comment
        fields = '__all__'

    def to_representation(self, instance: models.Comment):
        data = super(CommentSerializer, self).to_representation(instance)
        data['answers_count'] = self.Meta.model.objects.replies_all_count(instance=instance)
        if instance.file:
            data['file'] = {
                'src': instance.file.url,
                'content_type': None,
                'is_image': False
            }
            try:
                data['file']['content_type'] = mimetypes.guess_type(instance.file.url)[0]
                data['file']['is_image'] = 'image' in data['file']['content_type']
            except IndexError as e:
                pass
            except Exception as e:
                pass

        return data

    def validate(self, attrs):
        attrs.pop('recaptcha')
        return attrs
