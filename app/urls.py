from django.urls import path
from app import views
urlpatterns = [
   path('',views.index,name="index"),
   path('about/',views.about,name="about"),
   path('insert',views.insertData,name="insertData"),
   path('search',views.student_list,name="search"),
   path('update/<id>',views.updateData,name="updateData"),
   path('delete/<id>',views.deleteData,name="deleteData"),
   path('download/',views.export_to_excel,name="export_to_excel")
]