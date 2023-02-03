from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import Message, MessageVote, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'user',)
    search_fields = ('title', 'project', 'user')
    list_filter = ('project', 'user',)
    ordering = ('-created',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    def upvotes(self, obj):
        return obj.messagevote_set.filter(value=True).count()
    upvotes.short_description = 'Marcaram como "Gostei"'

    def downvotes(self, obj):
        return obj.messagevote_set.filter(value=False).count()
    downvotes.short_description = 'Marcaram como "Não Gostei"'

    list_display = ('user', 'topic', '__str__', 'upvotes', 'downvotes')
    search_fields = ('user', 'topic', 'message',)
    list_filter = ('user', 'topic',)
    ordering = ('-created',)


@admin.register(MessageVote)
class MessageVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'value',)
    search_fields = ('user', 'message', 'value',)
    list_filter = ('user', 'value',)
    ordering = ('-created',)
