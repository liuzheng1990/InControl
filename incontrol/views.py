from .models import *
from app_environment import AppEnvironment

class BaseView:
	# 设计基本输出逻辑。思考一下哪些信息应该整合输出。
	# 此类是显示层基类。输出逻辑的具体实现不必在这个类里给出。
	# 之后可以添加"CliView", "ApiView", "WebView", "MobileView"等等来实现具体的显示风格。
	def __init__(self, app):
		self.app = app


	# 先定义每一种基本类型的缩略显示，再
