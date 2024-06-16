from rest_framework.serializers import ValidationError


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, link):
        youtube_link = "https://youtube.com/"

        if link.get("link"):
            if youtube_link not in link.get("link"):
                raise ValidationError("Ссылка должна быть на youtube")
        else:
            return None
