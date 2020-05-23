import httplib2
import requests
import json

malware_path = 'testsafebrowsing.appspot.com/s/malware.html'
trusted_path = 'google.com'
host_url = 'http://localhost:8123/api/'
trusted_url = 'http://' + trusted_path
malware_url = 'http://' + malware_path
http = httplib2.Http()


def execute_get_request(url: str):
    headers = {'Content-Type': 'application/json'}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()


def execute_delete_request(url: str):
    headers = {'Content-Type': 'application/json'}
    resp = requests.delete(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()


def execute_post_request(url: str, payload: json):
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url, headers=headers, json=payload)
    print(resp)
    if resp.status_code == 200:
        return resp.json()


def get_hosts():
    return execute_get_request(host_url + 'hosts/')


def get_threats():
    return execute_get_request(host_url + 'threats/')


def get_blacklist():
    return execute_get_request(host_url + 'blacklist/')


def get_from_rule_list_by_host(list_json: json, host: str):
    for item in list_json:
        if str(item['host']) == host:
            return item


def get_threat_by_path(threats_json: json, http_path: str):
    for threat in threats_json:
        if threat['http_path'] == http_path:
            return threat


def add_host():
    execute_post_request(host_url + 'hosts/', {'host': 'dupa', 'ip': 'lol'})


def delete_host_from_blacklist(host_id: str):
    execute_delete_request(host_url + 'blacklist/' + host_id)


def test_adding_host_to_whitelist():
    return


def test_adding_host_to_blacklist():
    print(get_hosts()[0])


def test_malware_page():
    http.request(malware_url)
    threats = get_threats()
    expected_thread = get_threat_by_path(threats, malware_path)
    assert expected_thread is not None


def test_trusted_page():
    http.request(trusted_url)
    threats = get_threats()
    expected_thread = get_threat_by_path(threats, trusted_url)
    assert expected_thread is None


if __name__ == '__main__':
    test_malware_page()
    test_trusted_page()


