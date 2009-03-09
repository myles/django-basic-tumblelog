from django.contrib import admin

from tumblelog.models import *

admin.site.register(Item)

class LinkAdmin(admin.ModelAdmin):
	list_display	= ('title', 'url', 'author', 'publish')
	list_filter		= ('publish', 'author')
	search_fields	= ('title', 'body')

admin.site.register(Link, LinkAdmin)

class VideoSourceAdmin(admin.ModelAdmin):
	list_display	= ('title',)

admin.site.register(VideoSource, VideoSourceAdmin)

class VideoAdmin(admin.ModelAdmin):
	list_display	= ('title', 'author', 'publish')
	list_filter		= ('publish', 'author', 'source')
	search_fields	= ('title', 'body')

admin.site.register(Video, VideoAdmin)

class TwitterAdmin(admin.ModelAdmin):
	list_display	= ('title', 'author', 'publish')
	list_filter		= ('publish', 'author')
	search_fields	= ('body',)

admin.site.register(Twitter, TwitterAdmin)

class ChatAdmin(admin.ModelAdmin):
	list_display	= ('title', 'author', 'publish')
	list_filter		= ('publish', 'author')
	search_fields	= ('title', 'chat')

admin.site.register(Chat, ChatAdmin)

class EventAdmin(admin.ModelAdmin):
	list_display	= ('title', 'author', 'publish',)
	list_filter		= ('publish', 'author')
	search_fields	= ('title', 'body')

admin.site.register(Event, EventAdmin)

class PhotoAdmin(admin.ModelAdmin):
	list_display	= ('title', 'author', 'publish',)
	list_filter		= ('publish', 'author',)
	search_fields	= ('title', 'body')

admin.site.register(Photo, PhotoAdmin)

class AudioAdmin(admin.ModelAdmin):
	list_display	= ('title', 'author', 'publish')
	list_filter		= ('publish', 'author',)
	search_fields	= ('title', 'body')

admin.site.register(Audio, AudioAdmin)

class QuoteAdmin(admin.ModelAdmin):
	list_display	= ('title', 'author', 'publish')
	list_filter		= ('publish', 'author')
	search_fields	= ('quote', 'body')

admin.site.register(Quote, QuoteAdmin)

class SnippetAdmin(admin.ModelAdmin):
	list_display	= ('title', 'syntax', 'author', 'publish')
	list_filter		= ('publish', 'author')
	search_fields	= ('title', 'body', 'syntax')

admin.site.register(Snippet, SnippetAdmin)
