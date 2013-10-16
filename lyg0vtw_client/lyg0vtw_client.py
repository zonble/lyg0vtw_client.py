#!/usr/bin/env python
# encoding: utf-8

'A simple client for accessing api.ly.g0v.tw.'

import json
import unittest
try:
	import urllib.request as request
	import urllib.parse as urlparse
except:
	import urllib2 as request
	import urllib as urlparse

class LY_G0V_Client:
	BASE_URL = 'http://api-beta.ly.g0v.tw/v0/'
	# BASE_URL = 'http://api.ly.g0v.tw/v0/'

	def _fetch_data(self, url_path):
		URL = LY_G0V_Client.BASE_URL + url_path
		print(URL)
		f = request.urlopen(URL)
		r = f.read()
		return json.loads(r.decode('utf-8'))

	def fetch_all_bills(self):
		'Fetch all bills.'
		return self._fetch_data('collections/bills')

	def fetch_all_motions(self):
		'Fetch all motions.'
		return self._fetch_data('collections/motions')

	def fetch_bill(self, bill_id):
		'Fetch metadata of a specific bill.'
		assert(len(bill_id) > 0)
		return self._fetch_data('collections/bills/' + str(bill_id))

	def fetch_bill_data(self, bill_id):
		'Fetch data of a specific bill.'
		assert(len(bill_id) > 0)
		return self._fetch_data('collections/bills/' + str(bill_id) + '/data')

	def fetch_motions_related_with_bill(self, bill_id):
		'Fetch motions related with a specific bill.'
		assert(len(bill_id) > 0)
		query = json.dumps({'bill_ref': bill_id})
		query = urlparse.quote(query)
		return self._fetch_data('collections/motions/?q='+query)


class TestClient(unittest.TestCase):

	def setUp(self):
		self.client = LY_G0V_Client()
		print('setup')

	def test_all_bills(self):
		bills = self.client.fetch_all_bills()
		for key in ('entries', 'paging'):
			self.assertTrue(key in bills)
		for key in ('l', 'sk', 'count'):
			self.assertTrue(key in bills['paging'])
		for bill in bills:
			keys = ('abstract', 'data', 'proposal', 'updatedAt',
					'proposer', 'id', 'bill_id', 'createdAt',
					'petition', 'summary')
			self.assertTrue(key in bill)

	def test_all_motions(self):
		pass
	def test_fetch_bill(self):
		pass
	def test_fetch_bill_data(self):
		pass
	def test_fetch_motions_related_with_bill(self):
		pass


if __name__ == '__main__':
	unittest.main()

# client = LY_G0V_Client()
# print(client.fetch_all_motions())
# print(client.fetch_bill_data('1772G13550'))
# print(client.fetch_bill('1772G13550'))
# print(client.fetch_motions_related_with_bill('1772G13550'))
