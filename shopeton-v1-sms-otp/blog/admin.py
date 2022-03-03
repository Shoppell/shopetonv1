from django.contrib import admin
from blog.models import Comment, contact_with_us, Comment_shop, ticket, Category, SupCategory

admin.site.register(Category)
admin.site.register(SupCategory)
admin.site.register(Comment)
admin.site.register(contact_with_us)
admin.site.register(Comment_shop)
admin.site.register(ticket)
