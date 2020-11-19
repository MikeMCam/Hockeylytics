from django.contrib import admin
from .models import Post, PlayerList, Team, Match, Stats


admin.site.register(Post)
admin.site.register(PlayerList)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Stats)
