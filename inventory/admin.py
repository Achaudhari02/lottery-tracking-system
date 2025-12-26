from django.contrib import admin
from .models import Business, Store, Pack, Game, PackUpdate, UserProfile

# Register your models here.

# admin.site.register([Business, Store, Pack, Game, PackUpdate, UserProfile])

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name','owner')
    list_filter = ('name','owner')
    search_fields = ('name','owner')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name','business_name', 'store_code', 'is_active')
    list_filter = ('name','is_active')
    search_fields = ('name',)

    @admin.display(description="business_name")
    def business_name(self,obj):
        return obj.business.name
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'role','store_name')
    list_filter = ('role',)
    @admin.display(description='user_name')
    def user_name(self,obj):
        return obj.user.username
    
    @admin.display(description='store_name')
    def store_name(self,obj):
        return obj.store.name
    
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name','ticket_price','status','business_name')
    list_filter = ('name','status')

    @admin.display(description='business_name')
    def business_name(self,obj):
        return obj.business.name
    
@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ('pack_number','store_name','game_name')

    @admin.display(description="store")
    def store_name(self,obj):
        return obj.store.name
    
    @admin.display(description='game')
    def game_name(self,obj):
        return obj.game.name
    
admin.site.register(PackUpdate)