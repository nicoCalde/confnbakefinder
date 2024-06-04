from django.db import models
from django.conf import settings
import os

# Dictionary mapping neighborhoods to communes
NEIGHBORHOOD_COMMUNE = {
    'Retiro': '1', 'San Nicolás': '1', 'Puerto Madero': '1', 'San Telmo': '1', 'Montserrat': '1', 'Constitución': '1',
    'Recoleta': '2',
    'Balvanera': '3', 'San Cristóbal': '3',
    'La Boca': '4', 'Barracas': '4', 'Parque Patricios': '4', 'Nueva Pompeya': '4',
    'Almagro': '5', 'Boedo': '5',
    'Caballito': '6',
    'Flores': '7', 'Parque Chacabuco': '7',
    'Villa Soldati': '8', 'Villa Riachuelo': '8', 'Villa Lugano': '8',
    'Liniers': '9', 'Mataderos': '9', 'Parque Avellaneda': '9',
    'Villa Real': '10', 'Monte Castro': '10', 'Versalles': '10', 'Floresta': '10', 'Vélez Sarsfield': '10', 'Villa Luro': '10',
    'Villa General Mitre': '11', 'Villa Devoto': '11', 'Villa del Parque': '11', 'Villa Santa Rita': '11',
    'Coghlan': '12', 'Saavedra': '12', 'Villa Urquiza': '12', 'Villa Pueyrredón': '12',
    'Núñez': '13', 'Belgrano': '13', 'Colegiales': '13',
    'Palermo': '14',
    'Chacarita': '15', 'Villa Crespo': '15', 'La Paternal': '15', 'Villa Ortúzar': '15', 'Agronomía': '15', 'Parque Chas': '15',
}

# Tuples for choices
NEIGHBORHOODS = tuple((n, n) for n in NEIGHBORHOOD_COMMUNE.keys())
COMMUNES = tuple((i, str(i)) for i in range(1, 16))
CATEGORIES = (
    ('Chocolatería y Pastelería', 'Chocolatería y Pastelería'),
    ('Confitería y Café', 'Confitería y Café'),
    ('Confitería y Pan Tradicional', 'Confitería y Pan Tradicional'),
    ('Patisserie y Boulangerie', 'Patisserie y Boulangerie')
)
LOCAL_TYPES = [
    ('Cafetería', 'Cafetería'),
    ('Chocolatería', 'Chocolatería'),
    ('Crepería', 'Crepería'),
    ('Delicatessen', 'Delicatessen'),
    ('Panadería', 'Panadería'),
    ('Panadería Francesa', 'Panadería Francesa'),
    ('Pastelería', 'Pastelería'),
    ('Pastelería especializada en tartas nupciales', 'Pastelería especializada en tartas nupciales'),
    ('Pastelería francesa', 'Pastelería francesa'),
    ('Repostería', 'Repostería')
]

class CPC(models.Model):
    name = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=50, choices=NEIGHBORHOODS)
    commune = models.PositiveSmallIntegerField(choices=COMMUNES, editable=False)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    local_type = models.CharField(max_length=50, choices=LOCAL_TYPES)
    address = models.CharField(max_length=50)
    maps = models.URLField(max_length=300)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def delete(self, using=None, keep_parents=False):
        # Delete the image file when deleting the instance
        if self.image:
            self.image.delete(save=False)
        super().delete(using=using, keep_parents=keep_parents)