from db import Product, Requisites

product_not_found_message = '❌Товар с указанным ID не найден. Повторите попытку'

send_check_message = 'Пришлите чек (документом, т.е. без сжатия)\n\n' \
                     '❗В связи с учащением ' \
                     'количества совершаемых мошенниками преступлений, от вас могут потребоваться дополнительные ' \
                     'данные. В случае возникших вопросов с вами свяжется наш менеджер.'

not_valid_image = '❌Вы прислали некорректное изображение. Убедитесь что вы отправили изображение документом.'


def new_order_message(order_id: int, price: int):
    return f'Новый заказ #{order_id}\n' \
           f'Сумма: {price}BYN'


def product_founded_message(product: Product):
    result = f'✅Товар успешно найден!\nНаименование: {product.title}\n' \
             f'Стоимость: {product.price}BYN | {product.price}$\n\n' \
             f'Чтобы просмотреть доступные размеры или оформить заказ - нажмите на кнопку "Купить"'
    return result


def product_payout_message(data: Requisites, price):
    return f'❗Комиссии с платежей не взимаются. Для оплаты вам необходимо ' \
           f'найти раздел "ЕРИП" в интернет-банкинге.\n\n' \
           f'В каталоге ЕРИП:\n\n' \
           f'{data.detail}\n\nИ введите в поле реквизиты ниже:\n\n' \
           f'`{data.info}` <-- нажмите чтобы скопировать\n\n' \
           f'Сумма к оплате: {price}BYN\n\n' \
           f'📌После оплаты обязательно сохраните чек!'


def product_complete_message(order_id: int):
    return f'ID заказа: {order_id}\n' \
           f'Статус: "Ожидает модерации"\n' \
           f'После проверки вашего платежа, вы получите уведомление'
