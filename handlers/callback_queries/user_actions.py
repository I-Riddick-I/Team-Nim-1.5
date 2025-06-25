from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message

user_actions_router = Router(name='UserActionsRouter')


class UserAction(CallbackData, prefix='usr'):
    user_id: int


@user_actions_router.callback_query(UserAction.filter())
async def appeal(query: CallbackQuery, callback_data: UserAction):
    if not isinstance(message := query.message, Message):
        return
    if callback_data.user_id == query.from_user.id:
        await query.answer(text='Appeal sended')
        await message.delete_reply_markup()
    else:
        await query.answer(text='You cant appeal this message')
