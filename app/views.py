from django.shortcuts import render,redirect
from .models import Student
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse
import xlsxwriter
from io import BytesIO


# Create your views here.
def index(request):
    data=Student.objects.all()
    print(type(data))
    context={"data":data}
    print(type(context))
    return render(request,'index.html',context)

def insertData(request):
  
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        query=Student(name=name,email=email,age=age,gender=gender)
        query.save()
        messages.info(request,"Data inserted Successfully")
        return redirect("/")

        # print(name,email,age,gender)
    return render(request,'index.html')

def about(request):
    return render(request,"about.html")

def updateData(request,id):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        age=request.POST['age']
        gender=request.POST['gender']
        edit=Student.objects.get(id=id)
        edit.name=name
        edit.email=email
        edit.age=age
        edit.gender=gender
        edit.save()
        messages.warning(request,"Data Updated Successfully")
        return redirect("/")

    d=Student.objects.get(id=id)
    context={"d":d}

    return render(request,"edit.html",context)

def deleteData(request,id):
      d=Student.objects.get(id=id)
      d.delete()
      messages.error(request,"Deleted Successfully")
      return redirect("/")


def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(name__icontains=query)
    else:
        students = Student.objects.all()
    return render(request, 'search.html', {'data': students})

def export_to_excel(request):
    # Query the database to retrieve data
    queryset = Student.objects.all()

    # Convert queryset to DataFrame
    df = pd.DataFrame(list(queryset.values()))

    # Create a BytesIO buffer to store the Excel file
    excel_buffer = BytesIO()

    # Create Excel writer
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

    # Set the BytesIO buffer's position to the beginning
    excel_buffer.seek(0)

    # Serve the Excel file for download
    response = HttpResponse(excel_buffer.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=exported_data.xlsx'
    return response
