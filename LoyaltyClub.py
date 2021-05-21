from api.synchronizerAPI import SynchronizerAPI

s = SynchronizerAPI(('127.0.0.1', 8081))
s.start_serving()