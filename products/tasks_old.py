import yaml
import os
from celery import shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Product, Category, ProductAttribute, ProductAttributeValue
from suppliers.models import Supplier


@shared_task
def import_products_from_yaml(file_path, supplier_id):
    """Импорт товаров из YAML файла в формате спецификации"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        supplier = Supplier.objects.get(id=supplier_id)
        imported_count = 0
        
        # Определяем формат YAML файла
        if 'products' in data:
            # Формат sample_products.yaml
            return self._import_sample_format(data, supplier)
        elif 'categories' in data and 'goods' in data:
            # Формат спецификации API
            return self._import_specification_format(data, supplier)
        else:
            raise ValueError("Unsupported YAML format. Expected 'products' or 'categories'/'goods' structure.")
    
    def _import_sample_format(self, data, supplier):
        """Импорт из формата sample_products.yaml"""
        imported_count = 0
        
        for product_data in data.get('products', []):
            # Получаем или создаем категорию по имени
            category_name = product_data.get('category', 'Без категории')
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': f'Категория: {category_name}'}
            )
            
            # Создаем товар
            product = Product.objects.create(
                name=product_data['name'],
                description=product_data.get('description', ''),
                model=product_data.get('model', ''),
                sku=product_data.get('sku', ''),
                barcode=product_data.get('barcode', ''),
                category=category,
                supplier=supplier,
                price=product_data['price'],
                price_rrc=product_data.get('wholesale_price', product_data['price']),
                stock_quantity=product_data.get('stock_quantity', 0),
                min_order_quantity=product_data.get('min_order_quantity', 1),
                is_active=product_data.get('is_active', True)
            )
            
            # Обрабатываем характеристики товара
            attributes = product_data.get('attributes', {})
            for attr_name, attr_value in attributes.items():
                # Создаем атрибут если его нет
                attribute, created = ProductAttribute.objects.get_or_create(
                    name=attr_name,
                    defaults={
                        'type': 'text',
                        'is_required': False
                    }
                )
                
                # Создаем значение атрибута для товара
                ProductAttributeValue.objects.create(
                    product=product,
                    attribute=attribute,
                    value=str(attr_value)
                )
            
            imported_count += 1
        
        return imported_count
    
    def _import_specification_format(self, data, supplier):
        """Импорт из формата спецификации API"""
        imported_count = 0
        
        # Создаем категории
        category_map = {}
        for cat_data in data.get('categories', []):
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': f'Категория: {cat_data["name"]}'}
            )
            category_map[cat_data['id']] = category
        
        # Импортируем товары
        for product_data in data.get('goods', []):
            category = category_map.get(product_data['category'])
            
            # Создаем товар
            product = Product.objects.create(
                name=product_data['name'],
                model=product_data.get('model', ''),
                sku=str(product_data['id']),
                category=category,
                supplier=supplier,
                price=product_data['price'],
                price_rrc=product_data.get('price_rrc'),
                stock_quantity=product_data.get('quantity', 0),
                min_order_quantity=1,
                is_active=True
            )
            
            # Обрабатываем характеристики товара
            parameters = product_data.get('parameters', {})
            for param_name, param_value in parameters.items():
                # Создаем атрибут если его нет
                attribute, created = ProductAttribute.objects.get_or_create(
                    name=param_name,
                    defaults={
                        'type': 'text',
                        'is_required': False
                    }
                )
                
                # Создаем значение атрибута для товара
                ProductAttributeValue.objects.create(
                    product=product,
                    attribute=attribute,
                    value=str(param_value)
                )
            
            imported_count += 1
        
        return imported_count
                ProductAttributeValue.objects.get_or_create(
                    product=product,
                    attribute=attribute,
                    defaults={'value': str(param_value)}
                )
            
            imported_count += 1
        
        # Удаляем временный файл
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return f'Успешно импортировано {imported_count} товаров'
    
    except Exception as e:
        return f'Ошибка импорта: {str(e)}'


@shared_task
def export_products_to_yaml(supplier_id=None):
    """Экспорт товаров в YAML файл"""
    try:
        if supplier_id:
            products = Product.objects.filter(supplier_id=supplier_id)
            filename = f'products_export_supplier_{supplier_id}.yaml'
        else:
            products = Product.objects.all()
            filename = 'products_export_all.yaml'
        
        export_data = {
            'products': []
        }
        
        for product in products:
            product_data = {
                'name': product.name,
                'description': product.description,
                'sku': product.sku,
                'barcode': product.barcode,
                'category': product.category.name if product.category else '',
                'price': float(product.price),
                'wholesale_price': float(product.wholesale_price) if product.wholesale_price else None,
                'stock_quantity': product.stock_quantity,
                'min_order_quantity': product.min_order_quantity,
                'is_active': product.is_active,
                'attributes': {}
            }
            
            # Добавляем атрибуты
            for attr_value in product.attribute_values.all():
                product_data['attributes'][attr_value.attribute.name] = attr_value.value
            
            export_data['products'].append(product_data)
        
        # Сохраняем в файл
        yaml_content = yaml.dump(export_data, default_flow_style=False, 
                                allow_unicode=True, indent=2)
        
        file_path = f'exports/{filename}'
        saved_path = default_storage.save(file_path, ContentFile(yaml_content.encode('utf-8')))
        
        return f'Экспорт завершен. Файл сохранен: {saved_path}'
    
    except Exception as e:
        return f'Ошибка экспорта: {str(e)}'
