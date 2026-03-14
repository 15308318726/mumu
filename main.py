import time
import hashlib
import requests
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.clock import Clock
from kivy.utils import platform

# ====================== 配置区（改成你自己的）======================
NOTIFY_URL = "http://8.137.15.235:8080/notify.php"
PAY_KEY = "weixin123456"
CHECK_INTERVAL = 2
# =================================================================

class AutoCardApp(MDApp):
    def build(self):
        # 初始化界面和变量
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.last_order = ""
        self.running = False
        self.notification_text = ""  # 无障碍服务传递的通知内容

        # 主布局
        main_layout = MDBoxLayout(orientation="vertical", padding=20, spacing=15)
        
        # 标题
        main_layout.add_widget(MDLabel(
            text="微信收款自动发卡工具",
            font_size=24,
            halign="center",
            size_hint_y=0.2
        ))

        # 日志显示区域
        self.log_label = MDLabel(
            text="🔔 请先在【设置→无障碍→已下载的应用】开启本APP权限\n\n等待启动监听...",
            halign="left",
            valign="top",
            color=(0, 0, 0, 1)
        )
        scroll_view = MDScrollView(size_hint_y=0.6)
        scroll_view.add_widget(self.log_label)
        main_layout.add_widget(scroll_view)

        # 启动按钮
        self.start_btn = MDFillRoundFlatButton(
            text="启动监听",
            pos_hint={"center_x": 0.5},
            on_press=self.start_listen
        )
        main_layout.add_widget(self.start_btn)

        return main_layout

    # 日志输出（界面+控制台）
    def log(self, msg):
        print(msg)
        self.log_label.text += f"{time.strftime('%H:%M:%S')} - {msg}\n"
        self.log_label.texture_update()  # 刷新文本显示

    # 启动监听
    def start_listen(self, instance):
        if not self.running:
            self.running = True
            self.start_btn.text = "监听中（请勿关闭）"
            self.log("="*40)
            self.log("✅ 微信收款监听已启动")
            self.log(f"回调地址：{NOTIFY_URL}")
            self.log("="*40)
            # 定时检查通知
            Clock.schedule_interval(self.check_notification, CHECK_INTERVAL)

    # 检查并解析通知
    def check_notification(self, dt):
        if not self.running or not self.notification_text:
            return
        
        money, order_no = self.parse_money_and_order(self.notification_text)
        # 过滤有效收款（有金额+有订单号+非重复订单）
        if order_no and money > 0 and order_no != self.last_order:
            self.log(f"\n📩 检测到新收款")
            self.log(f"订单号：{order_no}")
            self.log(f"金额：{money} 元")

            # 通知发卡网
            result = self.send_notify(order_no, money)
            if result == "success":
                self.log("✅ 通知发卡网成功 → 已自动发卡！")
                self.last_order = order_no  # 标记为已处理
            else:
                self.log(f"❌ 通知失败：{result}")

    # 解析金额和订单号（复用你的核心逻辑）
    def parse_money_and_order(self, text):
        money = 0.0
        order_no = ""

        # 提取金额
        for line in text.split("\n"):
            if "¥" in line:
                money_str = line.split("¥")[-1].strip()
                try:
                    money = float(money_str)
                except:
                    pass

        # 提取18位数字订单号
        for line in text.split("\n"):
            line = line.strip()
            if len(line) >= 18 and line.isdigit():
                order_no = line
                break

        return money, order_no

    # 通知发卡网（复用你的核心逻辑）
    def send_notify(self, order_no, money):
        sign = hashlib.md5(f"{order_no}{money}{PAY_KEY}".encode()).hexdigest()
        params = {
            "order_no": order_no,
            "money": money,
            "sign": sign
        }
        try:
            res = requests.get(NOTIFY_URL, params=params, timeout=5)
            return res.text.strip()
        except Exception as e:
            return f"网络错误：{str(e)}"

    # 无障碍服务回调（接收通知）
    def on_notification(self, title, text):
        """由Java无障碍服务调用，接收微信通知"""
        if "微信收款" in title or "微信收款" in text:
            self.notification_text = f"{title}\n{text}"
            self.log(f"📱 收到微信通知：{title}")

if __name__ == "__main__":
    AutoCardApp().run()