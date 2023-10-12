from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.   在创建对象时使用
        create 方法： 当您在API中创建一个新对象时，create 方法被调用。它接受反序列化后的数据，并用这些数据创建一个新的对象，然后将其保存到数据库中。如果您不提供自定义的create方法，DRF将使用默认的创建逻辑
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.     在更新对象时使用
        update 方法： 当您在API中更新一个现有对象时，update 方法被调用。它接受一个现有对象实例和反序列化后的数据，并用数据更新对象的字段，然后将其保存到数据库中。如果您不提供自定义的update方法，DRF将使用默认的更新逻辑。
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance