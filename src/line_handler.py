# -*- coding: utf-8 -*-

from linebot import LineBotApi
from linebot.models import TextSendMessage
import json
import os


class LineHandler:
	def __init__(self):
		self.api_key_path = "../config/api_keys.json"
		self.access_token = self.load_access_token()

	def load_access_token(self):
		if os.path.exists(self.api_key_path):
			# ローカル実行の場合はjsonファイルからキーを取得する
			json_open = open(self.api_key_path, 'r')
			json_load = json.load(json_open)
			access_token = json_load["line_message_api"]["access_token"]
			return access_token
		else:
			# サーバで実行する際は環境変数から取得する
			return str(os.environ['LINE_MESSAGE_API_ACCESS_TOKEN'])

	def post_to_igarashi339(self, text):
		text = str(text)
		line_bot_api = LineBotApi(self.access_token)
		user_id = "U1fed3ee82231c47fce0de4a80f93c7be"
		messages = TextSendMessage(text=text)
		line_bot_api.push_message(user_id, messages=messages)
