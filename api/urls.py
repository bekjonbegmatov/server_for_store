
from django.urls import path
from django.urls import include
from . import views
urlpatterns = [
    # Admin
    path('', views.getRoutes , name="Imdex"),
    # Inventory Model
    path('inventory/<int:pk>', views.inventory_details, name='inventory_details'),
    path('inventory/all', views.getInventoryProducts, name='invAll'),
    path('inventory/create', views.createInventoryProduct, name="createInventoryProduct"),

    # Refund product from action to inventory
    path('refund' , views.refund_inventory_product , name='refund products'),

    path('actions/all', views.getActions, name="getActions"),
    path('action/<int:pk>', views.action_delete, name='inventory_details'),
    path('action/create', views.createAction, name="createAction"),

    path('kredit/all', views.getKreditdata, name="det duty"),
    path('kredit/create', views.createKredit, name="Create Kredit"),
    path('kredit/<int:pk>', views.kredit_details , name='inventory_details'),

    path('actions/export/excel', views.export_action_to_excel, name="export exsel action"),
    path('report/export/excel', views.report_actions_and_kresit_to_excel, name="export exsel action"),

    path('brlik/all', views.getBriliks, name='Barcha brlilani olish'),
    path('brlik/<int:pk>', views.brlik_detailes, name='brlik uzgartirish'),
    path('brlik/create', views.postBirlik , name=' clrate brlik'),

    path('note/all', views.get_notes_all , name=' get note'),
    path('note/create', views.post_notes , name=' clrate note'),
    path('note/<int:pk>', views.note_detals , name='inventory_details'),

    path('client/all', views.get_cliens , name='Get array of clients'),
    path('client/create', views.post_client , name='Added new client to the data base !'),
    path('client/<int:pk>', views.client_detals , name='change array method  put get delete'),

    path('client/action/all' , views.get_actions_of_client , name='get array about actions of clients' ),
    path('client/action/create' , views.post_actions_of_client , name='Post a new action'),
    path('client/action/<int:pk>' , views.actions_of_client_detals , name='change or delete action by id'),

]
