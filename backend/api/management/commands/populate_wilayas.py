from django.core.management.base import BaseCommand
from api.models import Shipping, Category, Material, PricingEngine
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates initial data for categories, materials, wilayas and pricing'

    def handle(self, *args, **options):
        # 1. Categories
        categories = [
            ("Walls", "جدران", "walls", "fa-paint-roller", 10),
            ("Doors", "أبواب", "doors", "fa-door-open", 15),
            ("Furniture", "أثاث", "furniture", "fa-sofa", 12),
            ("Ceilings", "أسقف", "ceilings", "fa-arrow-up", 10),
            ("Tiles", "بلاط", "tiles", "fa-border-all", 8),
            ("Kitchens", "مطابخ", "kitchens", "fa-utensils", 15),
            ("Cars", "سيارات", "cars", "fa-car", 20),
            ("Marble", "رخام", "marble", "fa-gem", 5),
            ("Geometric", "هندسي", "geometric", "fa-shapes", 15),
        ]
        for name_en, name_ar, slug, icon, waste in categories:
            Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name_en': name_en,
                    'name_ar': name_ar,
                    'icon': icon,
                    'waste_percent': waste
                }
            )
        self.stdout.write(self.style.SUCCESS('Categories populated'))

        # 2. Materials
        materials = [
            ("Standard Vinyl", "فينيل قياسي", "Economic option", 0, False),
            ("Premium Vinyl", "فينيل فاخر", "High durability", 500, True),
            ("Matte Finish", "مطفأ", "Non-reflective surface", 200, False),
            ("Glossy Finish", "لامع", "Shiny reflective surface", 200, False),
        ]
        for name_en, name_ar, desc, price, premium in materials:
            Material.objects.get_or_create(
                name_en=name_en,
                defaults={
                    'name_ar': name_ar,
                    'description': desc,
                    'price_per_m2': price,
                    'is_premium': premium
                }
            )
        self.stdout.write(self.style.SUCCESS('Materials populated'))

        # 3. Wilayas
        wilayas = [
            ("01", "أدرار", "Adrar"), ("02", "الشلف", "Chlef"), ("03", "الأغواط", "Laghouat"),
            ("04", "أم البواقي", "Oum El Bouaghi"), ("05", "باتنة", "Batna"), ("06", "بجاية", "Béjaïa"),
            ("07", "بسكرة", "Biskra"), ("08", "بشار", "Béchar"), ("09", "البليدة", "Blida"),
            ("10", "البويرة", "Bouira"), ("11", "تمنراست", "Tamanrasset"), ("12", "تبسة", "Tébessa"),
            ("13", "تلمسان", "Tlemcen"), ("14", "تيارت", "Tiaret"), ("15", "تيزي وزو", "Tizi Ouzou"),
            ("16", "الجزائر", "Alger"), ("17", "الجلفة", "Djelfa"), ("18", "جيجل", "Jijel"),
            ("19", "سطيف", "Sétif"), ("20", "سعيدة", "Saïda"), ("21", "سكيكدة", "Skikda"),
            ("22", "سيدي بلعباس", "Sidi Bel Abbès"), ("23", "عنابة", "Annaba"), ("24", "قالمة", "Guelma"),
            ("25", "قسنطينة", "Constantine"), ("26", "المدية", "Médéa"), ("27", "مستغانم", "Mostaganem"),
            ("28", "المسيلة", "M'Sila"), ("29", "معسكر", "Mascara"), ("30", "ورقلة", "Ouargla"),
            ("31", "وهران", "Oran"), ("32", "البيض", "El Bayadh"), ("33", "إليزي", "Illizi"),
            ("34", "برج بوعريريج", "Bordj Bou Arréridj"), ("35", "بومرداس", "Boumerdès"), ("36", "الطارف", "El Tarf"),
            ("37", "تندوف", "Tindouf"), ("38", "تيسمسيلت", "Tissemsilt"), ("39", "الوادي", "El Oued"),
            ("40", "خنشلة", "Khenchela"), ("41", "سوق أهراس", "Souk Ahras"), ("42", "تيبازة", "Tipaza"),
            ("43", "ميلة", "Mila"), ("44", "عين الدفلى", "Aïn Defla"), ("45", "النعامة", "Naâma"),
            ("46", "عين تموشنت", "Aïn Témouchent"), ("47", "غرداية", "Ghardaïa"), ("48", "غليزان", "Relizane"),
            ("49", "تيميمون", "Timimoun"), ("50", "برج باجي مختار", "Bordj Badji Mokhtar"),
            ("51", "أولاد جلال", "Ouled Djellal"), ("52", "بني عباس", "Béni Abbès"),
            ("53", "عين صالح", "In Salah"), ("54", "عين قزام", "In Guezzam"),
            ("55", "تقرت", "Touggourt"), ("56", "جانت", "Djanet"),
            ("57", "المغير", "El M'Ghair"), ("58", "المنيعة", "El Meniaa")
        ]
        for w_id, name_ar, name_fr in wilayas:
            Shipping.objects.update_or_create(
                wilaya_id=w_id,
                defaults={
                    'name_ar': name_ar,
                    'name_fr': name_fr,
                    'stop_desk_price': 400,
                    'home_delivery_price': 700
                }
            )
        self.stdout.write(self.style.SUCCESS('Wilayas populated'))

        # 4. Pricing Engine
        PricingEngine.objects.get_or_create(
            id=1,
            defaults={
                'raw_material_cost': 500,
                'labor_cost': 300,
                'international_shipping': 200
            }
        )
        self.stdout.write(self.style.SUCCESS('Pricing Engine initialized'))
