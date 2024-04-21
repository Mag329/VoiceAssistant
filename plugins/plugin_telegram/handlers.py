from aiogram import types, F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

import sys
import json

sys.path.append(r"../")
from plugins.plugin_smarthome.smarthome import *
from plugins.plugin_telegram.models import *


router = Router()

devices_name = []


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет!\n"
        "Я бот для управления умным домом Orange Home\n"
        "Список команд /help"
    )


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "Список команд:\n"
        "/start - Начало работы\n"
        "/help - Список команд\n"
        "/list - Управление умным домом\n"
    )


@router.message(Command("list"))
async def list_handler(message: Message, state: FSMContext):
    devices = Devices.query.order_by(Devices.id).all()

    global devices_name
    devices_name = [device.name for device in devices]

    await message.answer(
        text="Выберите устройство:", reply_markup=make_row_keyboard(devices_name)
    )
    await state.set_state(Control.choice_device_name)


@router.message(
    Control.choice_device_name,
    # F.text.in_(devices_name)
)
async def choice_device_name_handler(message: Message, state: FSMContext):
    await state.update_data(device_name=message.text)
    device_name = await state.get_data()
    print(device_name["device_name"])
    id = Devices.query.filter_by(name=device_name["device_name"]).first().id
    commands = Commands.query.filter_by(device_id=id).all().command
    await message.answer(
        "Теперь выберите функцию с которой хотите взаимодействовать:",
        reply_markup=make_row_keyboard(commands),
    )
    await state.set_state(Control.choice_device_func)


@router.message(
    Control.choice_device_func,
)
async def choice_command_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    ip = Devices.query.filter_by(name=data["device_name"]).first().ip
    command = (
        Commands.query.filter_by(
            name=data["device_name"],
        )
        .first()
        .command
    )
    await message.answer(
        text="Функция выполняется, подождите...", reply_markup=ReplyKeyboardRemove()
    )
    try:
        requests.get(f"http://{ip}{command}")
        await message.answer("Функция выполнена")
    except:
        await message.answer("Не удалось подключиться к устройству")

    await state.clear()


@router.message(Command("shoplist"))
async def shoplist_handler(message: Message):
    print("shoplist")
    with open("plugins/plugin_shoplist/list.json", encoding="utf8") as load_file:
        data = json.load(load_file)

        list = "Список покупок:\n"
        for i in data["list"]:
            lest += f'{i}. {i["name"]}, {i["amount"]}\n'

    await message.answer(list)
