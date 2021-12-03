from django.db import models
from django.db.models.fields import BigIntegerField

# Create your models here.

class Category(models.Model):
    initiator = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250, blank=True)
    country = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, default='Active')
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "category"


class Items(models.Model):
    initiator = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250, blank=True)
    #unit_price = models.CharField(max_length=250)
    #quantity = models.CharField(max_length=250)
    unit_price = models.FloatField(null=True)
    quantity =  models.IntegerField(null=True)
    pending_approval = models.CharField(max_length=250, default=0)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, default='Active')
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "item"



class ItemRequest(models.Model):
    requester = models.CharField(max_length=50, blank=True)
    item_name = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=150, blank=True)
    quantity_requested = models.IntegerField(blank=True)
    stage = models.CharField(max_length=30, default='pending')
    quantity_given = models.IntegerField(blank = True, default=0)
    manager_decision = models.CharField(max_length=20, default ='pending')
    head_decision = models.CharField(max_length=20, default ='pending')
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    
    
    def __str__(self):
        return self.item_name
    class Meta:
        db_table = "itemrequest"


class ManagerApproval(models.Model):
    request_id = models.CharField(max_length=254,  blank=True)
    inventManager = models.CharField(max_length=250,  blank=True)
    country = models.CharField(max_length=250,  blank=True)
    decision = models.CharField(max_length=20,  blank=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)     
    def __str__(self):
            return self.request_id

    class Meta:
        db_table = "managerapproval"
