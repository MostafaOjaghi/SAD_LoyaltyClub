from api.synchronizerAPI import SynchronizerAPI
from api.PointsDefinitionAPI import PointsDefinitionAPI
from PD.PointsDefinition import PointsDefinition
from db.DB import DBClass
import threading

DB = DBClass()
PD = PointsDefinition(DB)
sync_api = SynchronizerAPI(('127.0.0.1', 8081), DB)
pd_api = PointsDefinitionAPI(('127.0.0.1', 8082), DB, PD)
threading.Thread(target=lambda x: sync_api.start_serving(), args=(1,)).start()
threading.Thread(target=lambda x: pd_api.start_serving(), args=(1,)).start()
