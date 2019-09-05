"""
Как то так работает наша передача данных от пахо в бд и дальше на сайт..
"""

import paho.mqtt.client as mqtt
import json
from Worker import Worker, Base, Group
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    string = '807B859020000256/uart'    # Получаем номера карточек по сети и кидаем в бд.
    client.subscribe("devices/lora/#")


def on_message(client, userdata, msg):
    # lst -> Список карточек на площадках для отправки сигнала о подаче тока
    # Получаем по сети номера карт людей, и меняем занчение safe на обратное, один раз - в безопасности, второй - не в безопасности, и  по кргу.
    # Функция полу рабочая, не работает кнопка которая обозначает проведение взрывных работ, но мы поменяли ее на звонок диспетчеру, была ы кнопка, было бы больше автономности.
	parsed_str = json.loads(msg.payload)
	uid = parsed_str['data']['msg']
	lora_id = parsed_str['status']['devEUI']
	lst = ['1']
	w = s.query(Worker).filter(Worker.uid == uid).first()
	w.insafe = not w.insafe
	s.commit()
    # if uid in lst:
    #    gs = s.query(Group).filter(Group.lora_id == uid & Group.active == True).all()
    #    if len(gs) != 0:
    #        gs[0].button = True
    
    #w = s.query(Worker).filter(Worker.uid == uid).all()[0]
    #w = s.query(Worker).filter(Worker.uid == uid).first()

	#if w is not None:
	# w.insafe = not w.insafe
	# s.commit()




client = mqtt.Client()

# Поменяй бд на свой путь, по такому же примеру.
engine = create_engine('sqlite:////home/student/Крутяков_Антон/iot_proj/app.db')
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
s = session()

client.on_connect = on_connect
client.on_message = on_message
client.connect("10.11.162.100", 1883, 60)

client.loop_forever()
