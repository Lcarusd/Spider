# -*- coding:gbk -*-

import sys
from queue import Queue, Empty
import logging
import random
from threading import Thread
import urllib
import time
import json
import binascii
import requests
import hashlib
import struct
import pyDes
import binascii


def local_str(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    return value


def des_ecb_encrypt(data, key):
    des_entity = pyDes.des(key, mode=pyDes.ECB)
    padded = padding(data)
    return binascii.hexlify(des_entity.encrypt(padded))


def des_ecb_decrypt(data, key):
    data = data.strip().decode('hex')
    des_entity = pyDes.des(key, mode=pyDes.ECB)
    return des_entity.decrypt(data).replace('\x00', '')


def padding(data):
    remainder = len(data) % 8
    if remainder != 0:
        data += bytes('\x00') * (8-remainder)
    return data


class PlainRSA(object):

    def __init__(self, n, e):
        self.n = n
        self.e = e

    @classmethod
    def construct(cls, tup):
        n, e = tup
        return cls(n, e)

    def encrypt(self, data, K):
        return slow_rsa_encrypt(data, self.n, self.e), None


def slow_rsa_encrypt(data, n, e):
    """
    :param data:
    :param n:
    :param e:
    :return:
    """
    m = bytes_to_long(data)
    return long_to_bytes(pow(m, e, n))


def long_to_bytes(n, blocksize=0):
    """long_to_bytes(n:long, blocksize:int) : string
    Convert a long integer to a byte string.

    If optional blocksize is given and greater than zero, pad the front of the
    byte string with binary zeros so that the length is a multiple of
    blocksize.
    """
    # after much testing, this algorithm was deemed to be the fastest
    s = ''
    n = long(n)
    pack = struct.pack
    while n > 0:
        s = pack('>I', n & 0xffffffffL) + s
        n = n >> 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != '\000'[0]:
            break
    else:
        # only happens when n == 0
        s = '\000'
        i = 0
    s = s[i:]
    # add back some pad bytes.  this could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * '\000' + s
    return s


def bytes_to_long(s):
    """bytes_to_long(string) : long
    Convert a byte string to a long integer.

    This is (essentially) the inverse of long_to_bytes().
    """
    acc = 0L
    unpack = struct.unpack
    length = len(s)
    if length % 4:
        extra = (4 - length % 4)
        s = '\000' * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', s[i:i+4])[0]
    return acc
# --------------------------------------------------


class HongbaoException(Exception):

    def __init__(self, error_type, detail):
        self.error_type = error_type
        self.detail = detail

    def __str__(self):
        return 'HongbaoException: ErrorType:%s; Detail: %s' % \
               (self.error_type, self.detail)


class QQHongbao(object):

    DATA_ENCRYPT_KEY_V1 = '0d181064'

    QPAY_HONGBAO_ORDER_URL = "https://mqq.tenpay.com/cgi-bin/hongbao/qpay_hb_pack.cgi"
    QPAY_HONGBAO_PREPAY_URL = "https://myun.tenpay.com/cgi-bin/clientv1.0/qpay_gate.cgi"
    QPAY_BALANCE_PAY_URL = 'https://myun.tenpay.com/cgi-bin/clientv1.0/qpay_balance.cgi'
    QPAY_BANKCARD_PAY_URL = 'https://myun.tenpay.com/cgi-bin/clientv1.0/qpay_ydt.cgi'

    n = long(
        'B293AAC4108FF8637D9ECE9E064E8CE8F7728F914BBB2A3C5343733C63B7C51D98F7B2A8B5734E87E'
        '8F006F364CB54A80857783694F6515EB948871477EC4090EA11B7DF048016369ABD983256ACB9E809'
        '40727813B617FC7F3385415954682BB5E163FF8F3C62C10AE61FAB2980DDA4301BDA6DAA82307CC1D'
        '8D4A585F57D05', 16)
    e = long('010001', 16)
    rsa = PlainRSA.construct((n, e))

    DES_ENCRYPT_KEYS = (
        '9973e345',
        '5dac6cf7',
        'f5c88847',
        'f02c91bd',
        '3c0c3ea1',
        '8b00b67f',
        'c28931b2',
        'c8510256',
        'c42bfdef',
        '890fe53c',
        '0d181064',
        '0ef940b7',
        '10d75d6d',
        'c5d8e9f6',
        '66c3987e',
        'c48cebe3'
    )

    def __init__(self, qq_id, ws_app, bank_type=None, bind_serial=None):
        self.qq_id = qq_id
        self.ws_app = ws_app
        self.bank_type = bank_type
        self.bind_serial = bind_serial
        self.queue = Queue()

    def start(self):
        worker = Thread(target=self.run)
        worker.start()

    def run(self):
        logging.info('Start Run Hongbao worker: %s' % self.qq_id)
        while True:
            try:
                item = self.queue.get(block=True, timeout=10)
                if item:
                    skey = self.current_skey()
                    receiver, qun_id, amount, title, password, count = item
                    logging.info('QQHongbao:%s SendHongbao: receiver_id: %s, qun_id: %s, amount: %s, '
                                 'title: %s, skey: %s, count: %s' % (self.qq_id, receiver, qun_id,
                                                                     amount, title, skey, count))
                    resp = self.send_hongbao(
                        receiver, qun_id, amount, title, skey, password, count)
                    if 'mobile' in resp:
                        logging.info('NeedMobileVerificationCode:%s' % resp)
                        raise HongbaoException(
                            'NeedMobileVerificationCode', resp)
                    else:
                        time.sleep(3)
                else:
                    pass
            except Empty:
                pass
            except Exception as e:
                logging.exception(e)
                # sentry_except_handler(*sys.exc_info())
                time.sleep(10)

    def add_job(self, receiver_qq_id, qun_id, amount, title, password, count):
        self.queue.put(
            (receiver_qq_id, qun_id, amount, title, password, count))

    def send_hongbao(self, receiver, qun_id, amount, title, skey, password, count):
        password = local_str(password)
        token_id = self.fetch_token(
            receiver, qun_id, amount, title, skey, count)
        prepay_info = self.fetch_prepay_info(token_id, skey)
        qpay_skey = prepay_info['skey']
        trans_seq = int(prepay_info['trans_seq'])
        bank_infos = [(bank['bank_type'], bank['bind_serial'])
                      for bank in prepay_info.get('bind_banks', [])]
        qpay_balance = int(prepay_info['balance'])
        if qpay_balance >= amount * count:
            resp = self.pay_by_balance(
                password, token_id, trans_seq, qpay_skey)
        else:
            logging.info('No Enough Balance')
            if not bank_infos:
                raise HongbaoException("NoBankInfoAvailable", str)
            else:
                bank_type, bind_serial = bank_infos[0]
            resp = self.pay_by_bankcard(
                password, token_id, trans_seq, qpay_skey, bank_type, bind_serial)
        return resp

    # @classmethod
    # def current_skey(cls):
    #     cookies = CQSDK.GetCookies()
    #     return next((c.split('=')[1].strip() for c in cookies.split(';') if c.split('=')[0].strip() == 'skey'), '')

    def send_by_balance(self, receiver, qun_id, amount, title, skey, password, count=1):

        token_id = self.fetch_token(
            receiver, qun_id, amount, title, skey, count)
        qpay_skey, trans_seq, bank_infos = self.fetch_prepay_info(
            token_id, skey=skey)
        return self.pay_by_balance(password, token_id, trans_seq, qpay_skey)

    def send_by_bankcard(self, receiver, qun_id, amount, title, skey, password, count,
                         bank_type=None, bind_serial=None):
        token_id = self.fetch_token(
            receiver, qun_id, amount, title, skey, count)
        qpay_skey, des_key, bank_infos = self.fetch_prepay_info(
            token_id, skey=skey)

        if not bank_infos:
            raise ValueError("No BankInfo Available")
        else:
            if bank_type is None or bind_serial is None:
                bank_type, bind_serial = bank_infos[0]
            else:
                if not any(info for info in bank_infos if info[0] == bank_type and info[1] == bind_serial):
                    raise ValueError("ErrorInput BankdInfo: %s: %s" %
                                     (bank_type, bind_serial))

        return self.pay_by_bankcard(password, token_id, des_key, qpay_skey, bank_type, bind_serial)

    def fetch_token(self, receiver, qun_id, amount, title, skey, count):
        """
        {"retcode":"0","retmsg":"ok","is_confirm":"1","token_id":"1Vd1375b7ab887f0a39220704c38f6fd"}

        :param receiver:
        :param qun_id:
        :param amount:
        :param title:
        :param skey:
        :param count:
        :return:
        """
        args = [
            ("name", ""),
            ("total_amount", amount),
            ("total_num", count),
            ("bus_type", 2),
            ("type", 1),
            ("channel", 1024),
            ("grab_uin_list", receiver),
            ("wishing", title),
            ("recv_uin", qun_id),
            ("recv_type", 3),
            ("session_token", qun_id),
            ("uin", self.qq_id),
            ("h_model", "android_mqq"),
            ("h_edition", 42),
            ("h_location",
             "F69E69388684E9F48D1B60ECC8C63D9B||LON-AL00|4.4.4,sdk19||4FDC25FC605BBC5306B0AD466F90A415|1|"),
            ("h_qq_guid", "3121DF641DF9DFD93C05F77741BAD9C9"),
            ("h_qq_appid", "537045840"),
            ("h_exten", ""),
        ]

        _random = random.randint(0, 16)
        des_key = self.des_key_by_index(_random)
        data = des_ecb_encrypt('&'.join(["%s=%s" % (v[0], urllib.quote(str(v[1]))) for v in args]),
                               des_key).upper()
        params = {
            "ver": "2.0",
            "chv": "3",
            "req_text": data,
            "skey_type": "2",
            "random": _random,
            "skey": skey
        }
        resp = requests.post(self.QPAY_HONGBAO_ORDER_URL,
                             headers={}, data=params)
        decrypt_data = self.data_decrypt(resp.content, des_key)
        if 'token_id' in decrypt_data:
            return decrypt_data.get('token_id')
        else:
            logging.error('QQHongbao: %s: Failed Fetch TokenId: %s' %
                          (self.qq_id, decrypt_data))
            raise HongbaoException("NoTokenId", decrypt_data)

    def fetch_prepay_info(self, token_id, skey):
        """
        :param token_id:
        :param skey:
        :return:
        """
        args = (
            ("token_id", token_id),
            ("uin", self.qq_id),
            ("h_model", "android_mqq"),
            ("h_edition", 19),
            ("h_location",
             "F69E69388684E9F48D1B60ECC8C63D9B||LON-AL00|4.4.4,sdk19||4FDC25FC605BBC5306B0AD466F90A415|1|"),
            ("h_qq_guid", "3121DF641DF9DFD93C05F77741BAD9C9"),
            ("h_qq_appid", "537045840"),
            ("h_exten", ""),
            ("come_from", 2),
            ("h_location",
             "F69E69388684E9F48D1B60ECC8C63D9B||LON-AL00|4.4.4,sdk19||4FDC25FC605BBC5306B0AD466F90A415|1|"),
            ("h_qq_guid", "3121DF641DF9DFD93C05F77741BAD9C9"),
            ("h_qq_appid", "537045840"),
            ("h_exten", ""),
        )
        _random = random.randint(0, 16)
        des_key = self.des_key_by_index(_random)
        data = des_ecb_encrypt('&'.join(["%s=%s" % (v[0], urllib.quote(str(v[1]))) for v in args]),
                               des_key).upper()
        params = {
            "ver": "2.0",
            "chv": 3,
            "req_text": data,
            "skey_type": 2,
            "random": _random,
            "skey": skey,
        }
        resp = requests.post(self.QPAY_HONGBAO_PREPAY_URL,
                             headers={}, data=params)
        resp_json = des_ecb_decrypt(resp.content, des_key)
        result = json.loads(resp_json)
        return result

    def pay_by_balance(self, password, token_id, trans_seq, qpay_skey):
        """
        :return:
        """
        args = [
            ("p", self.password_encrypt(password)),
            ("token_id", token_id),
            ("is_reentry", 0),
            ("h_model", "android_mqq"),
            ("h_edition", 19),
            ("h_location",
             "F69E69388684E9F48D1B60ECC8C63D9B||LON-AL00|4.4.4,sdk19||4FDC25FC605BBC5306B0AD466F90A415|1|"),
            ("h_qq_guid", "3121DF641DF9DFD93C05F77741BAD9C9"),
            ("h_qq_appid", "537045840"),
            ("h_exten", ""),
        ]
        des_key = self.des_key_by_index(trans_seq)
        hb_data = des_ecb_encrypt('&'.join(["%s=%s" % (v[0], urllib.quote(str(v[1]))) for v in args]),
                                  des_key).upper()
        params = {
            "ver": "2.0",
            "chv": "3",
            "req_text": hb_data,
            "skey": qpay_skey,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Host": "myun.tenpay.com",
                   "Connection": "Keep-Alive"}
        resp = requests.post(self.QPAY_BALANCE_PAY_URL,
                             data=params, headers=headers)
        return self.data_decrypt(resp.content, des_key)

    def pay_by_bankcard(self, password, token_id, trans_seq, qpay_skey, bank_type, bind_serial):
        """
        :return:
        """
        args = [
            ("bank_type", bank_type),
            ("p", self.password_encrypt(password)),
            ("token_id", token_id),
            ("verify_flag", 2),
            ("bind_serial", bind_serial),
            ("is_reentry", 0),
            ("h_model", "android_mqq"),
            ("h_edition", 19),
            ("h_location",
             "F69E69388684E9F48D1B60ECC8C63D9B||LON-AL00|4.4.4,sdk19||4FDC25FC605BBC5306B0AD466F90A415|1|"),
            ("h_qq_guid", "3121DF641DF9DFD93C05F77741BAD9C9"),
            ("h_qq_appid", "537045840"),
            ("h_exten", ""),
        ]
        des_key = self.des_key_by_index(trans_seq)
        hb_data = des_ecb_encrypt('&'.join(["%s=%s" % (v[0], urllib.quote(str(v[1]))) for v in args]),
                                  des_key).upper()
        params = {
            "ver": "2.0",
            "chv": "3",
            "req_text": hb_data,
            "skey": qpay_skey,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Host": "myun.tenpay.com",
                   "Connection": "Keep-Alive"}

        resp = requests.post(self.QPAY_BANKCARD_PAY_URL,
                             headers=headers, data=params)
        return self.data_decrypt(resp.content, des_key)

    @classmethod
    def password_encrypt(cls, password):
        """
        :param password:
        """
        timestamp = str(int(time.time()))
        hex_timestamp = binascii.hexlify(timestamp).replace(' ', '')
        plain_text = '\x00\x05' + ''.join([chr(125) for _ in range(69)]) \
                     + chr(0) + timestamp + \
            ''.join([chr(255) for _ in range(14)]) + password
        rsa_encrypted = binascii.hexlify(
            cls.rsa.encrypt(plain_text, 1)[0]).upper()
        result = hex_timestamp + "F0D6C4CEE093903BFD05D6303A581B97E8442ABD" + rsa_encrypted
        return result

    @classmethod
    def send_bankcard(cls):
        pass

    @classmethod
    def data_encrypt(cls, args, key):
        data = des_ecb_encrypt('&'.join(["%s=%s" % (v[0], urllib.quote(str(v[1]))) for v in args]),
                               key).upper()
        return data

    @classmethod
    def data_decrypt(cls, data, key):
        decrypt_data = des_ecb_decrypt(data, key)
        print("--------------------------------------")
        print(decrypt_data)
        return json.loads(decrypt_data)

    @classmethod
    def des_key_by_index(cls, _random):
        return cls.DES_ENCRYPT_KEYS[_random % 16]


def decrypt_test(data):
    for key in QQHongbao.DES_ENCRYPT_KEYS:
        print(key)
        print(des_ecb_decrypt(data, key))


def md5_value(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


if __name__ == '__main__':
    qq_hongbao = QQHongbao(qq_id="1571239133", ws_app=None)
    skey = ""     # skey
    password = ""     # 支付密码

    for i in range(1):
        print(qq_hongbao.send_hongbao(
            receiver="",    # 红包接收人
            qun_id="", # 群账号
            amount=1,       # 金额大小
            title="",   # 文案
            skey=skey,
            password=md5_value(password),
            count=1
        ))
