from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
import xlwt
from . import export_to_excel

def index(request):
    return HttpResponse("<h1>Hello I'ts a first page</h1>")

@api_view(['GET'])
def getRoutes(request):
    # print(request)
    routes = [
        {
            'Developer': 'Begmatov Behruz',
            'Phone number': '+992920851515',
            'Git Hub': 'https://github.com/bekjonbegmatov',
            'FaceBook': '',
            'Instagram': 'https://www.instagram.com/behruz_1312_tj',
            'Telegram': 'https://t.me/behruz_begmatov',
            'Email': 'behruzbegmatov28@gmail.com',
        },
    ]
    return Response(routes)

def get_month(mon , year):
    date.today()
    ye = year
    months_range = mon
    m1 = date.today()
    m1 = str(m1)
    if str(mon) == "01":
        m1 = str(year)+'-' +str(months_range)+"-31"
    elif str(mon) == "02":
        m1 = str(year)+'-' + str(months_range)+"-28"
    elif str(mon) == "03":
        m1 =str(year)+'-' + str(months_range)+"-31"
    elif str(mon) == "04":
        m1 = str(year)+'-' + str(months_range)+"-30"
    elif str(mon) == "05":
        m1 = str(year)+'-' + str(months_range)+"-31"
    elif str(mon) == "06":
        m1 = str(year)+'-' + str(months_range)+"-30"
    elif str(mon) == "07":
        m1 = str(year)+'-' + str(months_range)+"-31"
    elif str(mon) == "08":
        m1 = str(year)+'-' + str(months_range)+"-31"
    elif str(mon) == "09":
        m1 = str(year)+'-' + str(months_range)+"-30"
    elif str(mon) == "10":
        m1 = str(year)+'-' + str(months_range)+"-31"
    elif str(mon) == "11":
        m1 = str(year)+'-' + str(months_range)+"-30"
    elif str(mon) == "12":
        m1 = str(year)+'-' + str(months_range)+"-31"
    return m1
        
@api_view(['GET'])
def getInventoryProducts(request):
    inventory = InventoryModel.objects.all()

    from_date = request.query_params.get('from_date', None)
    to_date = request.query_params.get('to_date', None)
    months_range = request.query_params.get('months', None)

    barcode = request.query_params.get('barcode', None)

    if to_date and from_date:
        date_format = '%d-%m-%Y'
        from_date = datetime.strptime(from_date, date_format)
        to_date = datetime.strptime(to_date, date_format)
        to_date += timedelta(days=1)

        inventory = InventoryModel.objects.filter(created__range=[from_date, to_date])
    elif months_range:
        dtoday = date.today()
        dtarget = dtoday + relativedelta(months=+(int(months_range)))
        dtarget += timedelta(days=1)

        inventory = InventoryModel.objects.filter(created__range=[dtoday, dtarget])
    elif barcode:
        inventory = InventoryModel.objects.filter(barcode=barcode)
        
    serializer = InventorySerializer(inventory, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createInventoryProduct(request):
    data = request.data
    print(data)
    serializer = InventorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print('------------------->>>' , serializer.data)
        return Response(serializer.data)
    print(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def getActions(request):
    action = ActionModel.objects.all()
    
    from_date = request.query_params.get('from_date', None)
    to_date = request.query_params.get('to_date', None)

    months_range = request.query_params.get('months', None)
    year = request.query_params.get('year', None)

    from_barcode = request.query_params.get('from_barcode' , None)
    to_barcode = request.query_params.get('to_barcode' , None)

    if from_barcode and to_barcode :
        if int(from_barcode) == 0:
            from_barcode = None
        if int(to_barcode) == 0:
            to_barcode = None

    if to_date and from_date:
        date_format = '%d-%m-%Y'
        from_date = datetime.strptime(from_date, date_format)
        to_date = datetime.strptime(to_date, date_format)
        to_date += timedelta(days=1)
        action = ActionModel.objects.filter(created__range=[from_date, to_date])
        if from_barcode and to_barcode :
            c = []
            for i in action:
                if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                    c.append(i) 
            action = c
    elif months_range and year:
        dtoday = date.today()
        dtarget = dtoday + relativedelta(months=+(int(months_range)))
        dtarget += timedelta(days=1)
        m1 = str(dtoday)
        m1 = str(year)+'-' +str(months_range)+"-01"
        action = ActionModel.objects.filter(created__range=[m1 , get_month(months_range , year)])
        if from_barcode and to_barcode :
            c = []
            n = from_barcode
            for i in action:
                if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                    c.append(i) 
            action = c
        # print(get_month(months_range) , m1)
    elif from_barcode and to_barcode :
        c = []
        n = from_barcode
        for i in ActionModel.objects.all():
            if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                c.append(i) 
        action = c
    serializer = ActionSerializer(action, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getDuty(request):
    duty = DutyModel.objects.all()
    serializer = DutySerializer(duty , many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createDuty(request):
    data = request.data
    print(data)
    serializer = DutySerializer(data=data)
    inventory = InventoryModel.objects.get(product_name=data['product_name'], barcode=data['barcode'])
    inventory.remained -= float(data['quantity'])
    inventory.sales +=float(data['quantity'])
    inventory.save()
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET' , 'PUT' , 'DELETE'])
def duty_detailes(request , pk):
    try:
        duty = DutyModel.objects.filter(id=pk)
    except DutyModel.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DutySerializer(duty , many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DutySerializer(duty, data=request.data)
        # print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        duty.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def createAction(request):
    data = request.data
    print("Data:", data)
    serializer = ActionSerializer(data=data)
    inventory = InventoryModel.objects.get(product_name=data['product_name'], barcode=data['barcode'])
    inventory.remained -= float(data['quantity'])
    inventory.sales +=float(data['quantity'])
    inventory.save()
    if serializer.is_valid():
        print("Foobarrrrrr")
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def action_delete(request , pk):
    try:
        action = ActionModel.objects.get(id=pk)
    except ActionModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        action.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def postBirlik(request):
    data = request.data
    print('data ==> :' , data)
    serializer = BrilikSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print("SAVED !!!!")
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def getBriliks(request):
    brlik = BirlikModel.objects.all()
    serializer = BrilikSerializer(brlik , many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def brlik_detailes(request, pk):
    try :
        brlik = BirlikModel.objects.get(id=pk)
    except BirlikModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BrilikSerializer(brlik , many=False)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = BrilikSerializer( brlik , data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        brlik.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def inventory_details(request, pk):
    try:
        inventory = InventoryModel.objects.get(id=pk)
    except InventoryModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InventorySerializer(inventory, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InventorySerializer(inventory, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        inventory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def export_action_to_excel(request):
    return export_to_excel.expot_action_to_exsel(request)

@api_view(['GET'])
def getKreditdata(request):

    from_date = request.query_params.get('from_date', None)
    to_date = request.query_params.get('to_date', None)

    months_range = request.query_params.get('months', None)
    year = request.query_params.get('year', None)

    from_barcode = request.query_params.get('from_barcode' , None)
    to_barcode = request.query_params.get('to_barcode' , None)

    user = request.query_params.get('user', None)

    kredit = KreditModel.objects.all() # import kredit model  

    if from_barcode and to_barcode :
        if int(from_barcode) == 0:
            from_barcode = None
        if int(to_barcode) == 0:
            to_barcode = None
    if from_date and to_date : 
        print('errorrrrr2')
        date_format = '%d-%m-%Y'
        from_date = datetime.strptime(from_date, date_format)
        to_date = datetime.strptime(to_date, date_format)
        to_date += timedelta(days=1)
        kredit = KreditModel.objects.filter(created__range=[from_date, to_date])
        if from_barcode and to_barcode :
            c = []
            for i in kredit:
                if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                    c.append(i) 
            kredit = c
    elif months_range and year :
        print('errorrrrr3')

        dtoday = date.today()
        dtarget = dtoday + relativedelta(months=+(int(months_range)))
        dtarget += timedelta(days=1)
        m1 = str(dtoday)
        m1 = str(year)+'-' +str(months_range)+"-01"
        kredit = KreditModel.objects.filter(created__range=[m1 , get_month(months_range , year)])
        if from_barcode and to_barcode :
            c = []
            n = from_barcode
            for i in kredit:
                if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                    c.append(i) 
            kredit = c
    elif from_barcode and to_barcode :
        print('errorrrrr4')

        c = []
        n = from_barcode
        for i in KreditModel.objects.all():
            if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                c.append(i) 
        kredit = c
    if user:
        kredit = KreditModel.objects.filter(client=user)
    serializer = KreditSerializer(kredit , many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def kredit_details(request, pk):
    """
    Retrieve, update or delete a inventory_details.
    """
    try:
        kredit = KreditModel.objects.get(id=pk)
    except KreditModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = KreditSerializer(kredit, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        
        print(data)
        serializer = KreditSerializer(kredit, data=request.data)
        # print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        kredit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def createKredit(request):
    data = request.data
    serializer = KreditSerializer(data=data)
    inventory = InventoryModel.objects.get(product_name=data['product_name'], barcode=data['barcode'])
    inventory.remained -= float(data['quantity'])
    inventory.sales +=float(data['quantity'])
    inventory.save()
    if serializer.is_valid():
        print("Foobarrrrrr")
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

def report_actions_and_kresit_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=" ' + str(date.today()) + ' inventory.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Inventory')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [ 'Штрих код' , 'Название' , 'Кол-ва' , 'Цена(прод)' , 'Cозданo' ,  'Oплачено' , 'Цена(покупка)' , 'Цена(тела)' , 'Цена(прод.общ)' , 'Цена(покупка.общ)' , 'Цена(тела.общ)' , 'Общ.количество']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    rows = []
    total_price = 0
    total_del_price = 0
    total_body_price = 0
    total_quantity = 0
    for i in ActionModel.objects.all():
        temp = []
        temp.append(i.barcode)
        temp.append(i.product_name)
        temp.append(i.quantity)
        temp.append(i.selling_price)
        temp.append(str(i.created)[0:10])
        temp.append(i.paid)
        temp.append(i.del_price)
        temp.append(i.body_price)
        temp.append("")
        temp.append("")
        temp.append("")
        temp.append("")
        total_price += float(i.selling_price)
        total_del_price += float(i.del_price)
        total_body_price += float(i.body_price)
        total_quantity += int(i.quantity)
        rows.append(temp)
    total = []
    for i in range(8):
        total.append("")
    total.append(total_price)
    total.append(total_del_price)
    total.append(total_body_price)
    total.append(total_quantity)
    rows.append(total)

    colims_of_kredit = ['id' ,'Имя', 'Штрих код' , 'Название' , 'Кол-ва' , 'Телефон номер' , 'Cозданo' , 'Oплачено' , 'Цена' , 'На долге' , 'Общая цена'  , 'Общ.количество']
    rows.append('')
    rows.append("Долг")
    rows.append('')

    temp1 = [] 
    for i in colims_of_kredit:
        temp1.append(i)
    rows.append(temp1)
    temp1 = []
    final_price = 0
    filar_quantity = 0
    for i in KreditModel.objects.all():
        temp = []
        temp.append(i.id)
        temp.append(i.client)
        temp.append(i.barcode)
        temp.append(i.product_name)
        temp.append(i.quantity)
        temp.append(i.phone_number)
        temp.append(str(i.created)[0:10])
        temp.append(i.paid)
        temp.append(i.final_price)
        if i.c == True:
            temp.append('Да')
        else:
            temp.append('Нет')
        temp.append('')
        temp.append('')
        final_price += i.final_price
        filar_quantity += i.quantity
        rows.append(temp)
    for i in range(len(colims_of_kredit)-2):
        temp1.append('')
    temp1.append(final_price)
    temp1.append(filar_quantity)
    rows.append(temp1)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

# Note
@api_view(['GET'])
def get_notes_all(request):
    notes = NotesModel.objects.all()
    serializer = NotesSerializer(notes , many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_notes(request):
    data = request.data
    serializer = NotesSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def note_detals(request , pk):
    try:
        note = NotesModel.objects.get(id=pk)
    except NotesModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = NotesSerializer(note , many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data
        serializer = NotesSerializer(note , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_cliens(request):
    client = ClientModel.objects.all()
    serializer = ClientSetializer(client , many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_client(request):
    data = request.data
    try:
        ClientActionModel.objects.get(client=data['client'] , phone_number=data['phone_number'])
    except ClientActionModel.DoesNotExist:
        serializer = ClientSetializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET' , 'PUT' , 'DELETE'])
def client_detals(request , pk):
    try:
        client = ClientModel.objects.get(id=pk)
    except ClientModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        data = request.data
        serializer = ClientSetializer(client , data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'GET':
        serializer = ClientSetializer(client , many=False)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_actions_of_client(request):
    months_range = request.query_params.get('months', None)
    year = request.query_params.get('year', None)
    user = request.query_params.get('user', None)

    from_date = request.query_params.get('from_date', None)
    to_date = request.query_params.get('to_date', None)

    from_barcode = request.query_params.get('from_barcode' , None)
    to_barcode = request.query_params.get('to_barcode' , None)

    action = ClientActionModel.objects.all()

    if from_barcode and to_barcode :
        if int(from_barcode) == 0:
            from_barcode = None
        if int(to_barcode) == 0:
            to_barcode = None
    if to_date and from_date:
        date_format = '%d-%m-%Y'
        from_date = datetime.strptime(from_date, date_format)
        to_date = datetime.strptime(to_date, date_format)
        to_date += timedelta(days=1)
        action = ClientActionModel.objects.filter(created__range=[from_date, to_date])
        if from_barcode and to_barcode :
            c = []
            for i in action:
                if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                    c.append(i) 
            action = c
    elif from_barcode and to_barcode :
        c = []
        n = from_barcode
        for i in ClientActionModel.objects.all():
            if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                c.append(i) 
        action = c
    elif user and months_range and year :
        action = ClientActionModel.objects.filter(client=user)
        dtoday = date.today()
        dtarget = dtoday + relativedelta(months=+(int(months_range)))
        dtarget += timedelta(days=1)
        m1 = str(dtoday)
        m1 = str(year)+'-' +str(months_range)+"-01"
        action = action.filter(created__range=[m1 , get_month(months_range , year)])
        # print(action)
    elif user:
        action = ClientActionModel.objects.filter(client=user)

    elif months_range and year:
        dtoday = date.today()
        dtarget = dtoday + relativedelta(months=+(int(months_range)))
        dtarget += timedelta(days=1)
        m1 = str(dtoday)
        m1 = str(year)+'-' +str(months_range)+"-01"
        action = ClientActionModel.objects.filter(created__range=[m1 , get_month(months_range , year)])

    serializer = ClientActionSerializer(action , many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_actions_of_client(request):
    data = request.data
    serializer = ClientActionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['PUT' , 'GET' , 'DELETE'])
def actions_of_client_detals(request , pk):
    try:
        action = ClientActionModel.objects.get(id=pk)
    except ClientActionModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        data = request.data
        serializer = ClientActionSerializer(action , data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'GET':
        serializer = ClientActionSerializer(action , many=False)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        action.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def report_all_models(request):

    action = ActionModel.objects.all()
    # action += KreditModel.objects.all()
    from_date = request.query_params.get('from_date', None)
    to_date = request.query_params.get('to_date', None)

    months_range = request.query_params.get('months', None)
    year = request.query_params.get('year', None)

    from_barcode = request.query_params.get('from_barcode' , None)
    to_barcode = request.query_params.get('to_barcode' , None)

    if from_barcode and to_barcode :
        if int(from_barcode) == 0:
            from_barcode = None
        if int(to_barcode) == 0:
            to_barcode = None

    if to_date and from_date:
        date_format = '%d-%m-%Y'
        from_date = datetime.strptime(from_date, date_format)
        to_date = datetime.strptime(to_date, date_format)
        to_date += timedelta(days=1)
        action = ActionModel.objects.filter(created__range=[from_date, to_date])
        if from_barcode and to_barcode :
            c = []
            for i in action:
                if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                    c.append(i) 
            action = c
    elif months_range and year:
        dtoday = date.today()
        dtarget = dtoday + relativedelta(months=+(int(months_range)))
        dtarget += timedelta(days=1)
        m1 = str(dtoday)
        m1 = str(year)+'-' +str(months_range)+"-01"
        action = ActionModel.objects.filter(created__range=[m1 , get_month(months_range , year)])
        if from_barcode and to_barcode :
            c = []
            n = from_barcode
            for i in action:
                if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                    c.append(i) 
            action = c
        # print(get_month(months_range) , m1)
    elif from_barcode and to_barcode :
        c = []
        n = from_barcode
        for i in ActionModel.objects.all():
            if int(from_barcode) <= int(i.barcode) <= int(to_barcode) :
                c.append(i) 
        action = c
    serializer = ActionSerializer(action, many=True)
    return Response(serializer.data) 

@api_view(['POST', 'GET'])
def refund_inventory_product(request):
    if request.method == 'GET':
        routes = [
            {
                'Developer': 'Begmatov Behruz',
                'Phone number': '+992920851515',
                'Git Hub': 'https://github.com/bekjonbegmatov',
                'FaceBook': '',
                'Instagram': 'https://www.instagram.com/behruz_1312_tj',
                'Telegram': 'https://t.me/behruz_begmatov',
                'Email': 'behruzbegmatov28@gmail.com',
            },
        ]
        return Response(routes)
    data = request.data
    inventory = InventoryModel.objects.get(product_name=data['product_name'], barcode=data['barcode'])
    inventory.remained += float(data['quantity'])
    inventory.sales -=float(data['quantity'])
    inventory.save()

    try:
        action = ActionModel.objects.get(id=data['id'])
    except ActionModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    action.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


