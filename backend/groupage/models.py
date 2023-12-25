from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Max, Sum
from django.db.models.signals import post_delete, post_save
from datetime import date, datetime
from src.methods import *
from app.models import *

def getNextNumber(prefix,model):
    all = model.objects.filter(date_creation__year = date.today().year).order_by("numero")
    last = all.last()

    if not last or (last.date_creation.year != date.today().year):
        return prefix+'000001'
    else: 
        max = 0
        for record in all: 
            if int(record.numero.split(prefix)[-1]) > max : 
                max = int(record.numero.split(prefix)[-1]) 

        new_int = max + 1
        new_no = prefix + format(new_int, '06d')

    return new_no 


def getNumeroVisiteGroupage():
    return getNextNumber('V/GROUPAGE',VisiteGroupage)

def getNumeroFacture():
    pass

class VisiteGroupage(models.Model):
    TYPES_VISITE = [
        ('Visite douane', 'Visite douane'),
        ('Visite D41', 'Visite D41'),
    ]
    visite = models.CharField(max_length=50, blank=True, null=True, unique=True)
    numero = models.CharField(max_length=17, default=getNumeroVisiteGroupage)
    date_creation = models.DateField(auto_now_add=True)
    date_visite = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now)
    gros = models.ForeignKey("app.Gros", on_delete=models.PROTECT)
    article = models.ForeignKey("app.Article", on_delete=models.CASCADE, blank=True, null=True)
    sous_article = models.ForeignKey("app.SousArticle", on_delete=models.CASCADE, blank=True, null=True)
    type_visite = models.CharField(max_length=15, choices=TYPES_VISITE)
    transitaire = models.ForeignKey("reference.Transitaire", on_delete=models.PROTECT)
    badge = models.CharField(max_length=50)
 
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "viites"
        
    def clean(self):
            records_count = VisiteGroupage.objects.filter(date_creation__year = date.today().year,numero = self.numero).count()
            if records_count > 0: 
                raise ValidationError({"numero":"Visite aleady exist."})

    def __str__(self):
        return self.numero

    def save(self, *args, **kwargs):
        self.visite = self.numero + " / " + str(self.date_visite.year)
            
        super(VisiteGroupage, self).save(*args, **kwargs)

class PositionGroupage(models.Model): 
    sous_article = models.ForeignKey("app.SousArticle", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    box = models.ForeignKey("reference.Box", on_delete=models.CASCADE)
    
    def update_sous_article_position(self): 
        self.sous_article.box = self.box 
        self.sous_article.save()
    
    def __str__(self):
        return str(self.box) + " " + str(self.date) 
    
def post_save_position_groupage(sender, instance,**kwargs): 
        instance.update_sous_article_position()

post_save.connect(post_save_position_groupage, sender = PositionGroupage)