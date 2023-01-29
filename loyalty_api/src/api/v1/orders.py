from fastapi import APIRouter, Depends

from src.services.orders import OrderService, get_order_service
from src.models.order import orders


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get('/test',
            # response_model=PromoCode,
            summary="",
            description="",
            )
async def promo_details(order_service: OrderService = Depends(get_order_service)):
    """
    Возвращает информацию по одному промокоду
    """
    query = orders.select()
    print(query)
    res = await order_service.fetch(query=query)
    res = [item.id for item in res]
    return {'query': str(query), 'res': res}
