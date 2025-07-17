import json
import pickle


def decode_blob(blob_data):
    try:
        decoded_data = json.loads(blob_data.decode('utf-8'))
        return decoded_data
    except (UnicodeDecodeError, json.JSONDecodeError):
        try:
            decoded_data = pickle.loads(blob_data)
            return decoded_data
        except pickle.UnpicklingError:
            return None
    except Exception as e:
        return None


def array_to_blob(array):
    return pickle.dumps(array)
