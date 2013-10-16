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

	def _test_bill(self, bill):
		keys = ('proposed_by', 'doc', 'abstract', 'sponsors',
				'summary', 'bill_ref', 'motions', 'cosponsors',
				'bill_id');
		for key in keys:
			self.assertTrue(key in bill)
		if isinstance(bill['doc'], dict):
			self.assertTrue('pdf' in bill['doc'])
			self.assertTrue('doc' in bill['doc'])

	def _test_motion(self, motion):
		keys = ('result', 'resolution', 'motion_class', 'bill_id',
				'agenda_item', 'bill_ref', 'tts_id',
				'subitem', 'status', 'sitting_id', 'item',
				'summary', 'tts_seq', 'proposed_by', 'doc')
		for key in keys:
			self.assertTrue(key in motion, key)
		if isinstance(motion['doc'], dict):
			self.assertTrue('pdf' in motion['doc'])
			self.assertTrue('doc' in motion['doc'])

	def _test_motions(self, motions):
		for key in ('entries', 'paging'):
			self.assertTrue(key in motions)
		for key in ('l', 'sk', 'count'):
			self.assertTrue(key in motions['paging'])
		for motion in motions['entries']:
			self._test_motion(motion)

	def test_all_bills(self):
		bills = self.client.fetch_all_bills()
		for key in ('entries', 'paging'):
			self.assertTrue(key in bills)
		for key in ('l', 'sk', 'count'):
			self.assertTrue(key in bills['paging'])
		for bill in bills['entries']:
			self._test_bill(bill)

	def _test_data(self, data):
		for key in ('related', 'content'):
			self.assertTrue(key in data)
		self.assertTrue(isinstance(data['related'], list))
		self.assertTrue(isinstance(data['content'], list))
		for item in data['content']:
			content_keys = ('name', 'type', 'content', 'header')
			for content_key in content_keys:
				self.assertTrue(content_key in item)
			self.assertTrue(len(item['name']) > 0)
			self.assertTrue(isinstance(item['name'], str))
			self.assertTrue(len(item['type']) > 0)
			self.assertTrue(isinstance(item['type'], str))
			self.assertTrue(len(item['content']) > 0)
			self.assertTrue(isinstance(item['content'], list))
			for content in item['content']:
				self.assertTrue(isinstance(content, list))
				for line in content:
					self.assertTrue(isinstance(line, str))
			self.assertTrue(len(item['header']) > 0)
			self.assertTrue(isinstance(item['header'], list))
			for header in item['header']:
				self.assertTrue(isinstance(header, str))

	def test_all_motions(self):
		motions = self.client.fetch_all_motions()
		self._test_motions(motions)

	def test_fetch_bill(self):
		bill = self.client.fetch_bill('1772G13550')
		self._test_bill(bill)

	def test_fetch_bill_data(self):
		data = self.client.fetch_bill_data('1772G13550')
		self._test_data(data)

	def test_fetch_motions_related_with_bill(self):
		motions = self.client.fetch_motions_related_with_bill('1772G13550')
		self._test_motions(motions)


if __name__ == '__main__':
	unittest.main()
