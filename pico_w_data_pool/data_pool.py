import gc
import ujson as json
import urequests
import network
import time

class DataPool:
    def __init__(self, config_path='config.json'):
        self.load_config(config_path)
        self.pools = [[]]
        self.current_pool_idx = 0

    def load_config(self, path):
        with open(path) as f:
            config = json.load(f)
        self.pool_capacity = config['pool_capacity']
        self.process_mode = config['process_mode']
        self.server_url = config['server_url']
        self.warn_pool_count = config.get('warn_pool_count', 2)
        self.fetch_retry_count = config.get('fetch_retry_count', 5)

    def get_max_pool_count(self):
        free_mem = gc.mem_free()
        pool_size_bytes = self.pool_capacity * 1000
        return max(1, free_mem // pool_size_bytes)

    def check_and_warn(self):
        max_pool_count = self.get_max_pool_count()
        available = max_pool_count - len(self.pools)
        if available < self.warn_pool_count:
            self.send_warning(available)

    def server_received_data(self, data):
        if data.startswith('{') or data.startswith('['):
            try:
                json_data = json.loads(data)
                status = 400
                if isinstance(json_data, dict) and 'index' in json_data:
                    index = json_data['index']
                    if isinstance(index, int) and 0 <= index < len(self.pools):
                        status = self.send_data(self.pools[index])
            except Exception as e:
                print('JSON decode error:', e)
                status = 500
            return status

    def add_data(self, data):
        pool = self.pools[self.current_pool_idx]
        pool.append(data)
        if len(pool) >= self.pool_capacity:
            index = self.current_pool_idx if self.process_mode == 'B' else None
            self.process_pool(pool, index)
            if len(self.pools) < self.get_max_pool_count():
                self.pools.append([])
                self.current_pool_idx += 1
                self.check_and_warn()
            else:
                self.current_pool_idx = 0
                self.pools[self.current_pool_idx] = []

    def process_pool(self, pool, index=None):
        if self.process_mode == 'A':
            self.send_data(pool)
        elif self.process_mode == 'B':
            self.request_server_fetch(pool, index)
        pool.clear()

    def send_data(self, pool):
        try:
            print('server_url:', self.server_url)
            print('pool data:', pool)
            resp = urequests.post(self.server_url, json=pool)
            status = resp.status_code
            print('Data sent:', status)
            resp.close()
        except Exception as e:
            print('Send error:', e)
            status = 500
        return status

    def request_server_fetch(self, pool, index=None):
        try:
            resp = urequests.post(self.server_url + '/fetch', json={'count': len(pool), 'index': index})
            print('Fetch requested:', resp.status_code)
            retry = self.fetch_retry_count
            status = 200
            while retry > 0:
                check = urequests.get(self.server_url + '/fetch_status')
                if check.json().get('status') == 'done':
                    check.close()
                    break
                check.close()
                time.sleep(2)
                retry -= 1
            resp.close()
            if retry == 0:
                print('Fetch timeout')
                status = 500
        except Exception as e:
            print('Fetch error:', e)
            status = 500
        return status

    def send_warning(self, available):
        try:
            warn_url = self.server_url + '/warn'
            payload = {'available_pool_count': available}
            resp = urequests.post(warn_url, json=payload)
            status = resp.status_code
            print('Warning sent:', status)
            resp.close()
        except Exception as e:
            print('Warning error:', e)
            status = 500
        return status

data_pool = DataPool()

def add_data(json_obj):
    data_pool.add_data(json_obj)
