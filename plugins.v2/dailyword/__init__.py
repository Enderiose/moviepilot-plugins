import base64
import time
from datetime import datetime
from typing import List, Tuple, Dict, Any, Optional
from urllib.parse import urlsplit

import requests

from app.log import logger
from app.plugins import _PluginBase

# ---------------------------------------------------------------------------
# 图片源（netstorm 2026-11-19 实测）
#
#   img_url 形如 http://image.wufazhuce.com/xxxx，浏览器直连时 DNS 解析到
#   国内七牛节点 120.220.194.41，该链路大面积连接重置：
#       PC       http 0/8   https 3/8
#       容器内   http 0/6   https 1/6
#   强制解析到七牛海外节点 154.41.93.240 / .241：
#       PC / 容器 http 8/8   https 8/8
#
#   浏览器无法自定义 Host 头，所以这里由后端下载图片 → base64 内嵌，
#   前端 VImg 直接渲染 data URI，彻底不依赖浏览器到 CDN 的链路。
#
#   海外 IP 若变更，用 DoH 重查：
#     curl -s -x http://192.168.2.4:7890 -H "accept: application/dns-json" \
#       "https://cloudflare-dns.com/dns-query?name=image.wufazhuce.com&type=A"
# ---------------------------------------------------------------------------
_IMAGE_HOST = "image.wufazhuce.com"
_IMAGE_EDGE_HOSTS = ("154.41.93.240", "154.41.93.241")
# 七牛图片处理参数：宽 800，约 30KB（原图约 800KB）
_IMAGE_RESIZE = "?imageView2/2/w/800"

# 成功结果缓存 24 小时；失败只缓存 60 秒 —— 刷新即可重试。
# 原版用 lru_cache 把「失败回退值」缓存一整天，导致当天第一次失败后
# 无论刷新多少次都不会再重试，这是「经常刷不出图」的直接原因。
_TTL_OK = 86400
_TTL_FAIL = 60
_TTL_API_FAIL = 300

# 进程内缓存：key -> (过期时间戳, 值)
_cache: Dict[str, Tuple[float, Any]] = {}


def _cache_get(key: str) -> Tuple[Any, bool]:
    """读缓存，返回 (值, 是否命中)。"""
    hit = _cache.get(key)
    if not hit:
        return None, False
    if hit[0] <= time.time():
        _cache.pop(key, None)
        return None, False
    return hit[1], True


def _cache_put(key: str, value: Any, ttl: int) -> Any:
    """写缓存并返回该值。"""
    _cache[key] = (time.time() + ttl, value)
    if len(_cache) > 64:
        now = time.time()
        for k in [k for k, v in _cache.items() if v[0] <= now]:
            _cache.pop(k, None)
    return value


def _http_get(url: str, host: Optional[str] = None, timeout: int = 15):
    """
    GET 请求，显式禁用环境变量代理与系统代理。

    容器内若继承 http_proxy 会走 192.168.2.4:7890，实测该路径返回 000。
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    }
    if host:
        headers["Host"] = host
    try:
        session = requests.Session()
        session.trust_env = False
        return session.get(url, headers=headers, timeout=timeout,
                           proxies={"http": None, "https": None})
    except Exception as err:
        logger.debug(f"每日一言请求失败 {url}: {err}")
        return None


def _download_image(img_url: str) -> Optional[bytes]:
    """
    下载图片，多源依次尝试，每个源重试 2 次：
      1. 七牛海外节点 http（主力，实测 8/8）
      2. 域名 https（兜底，国内节点成功率低）
    先试带压缩参数（约 30KB），失败再试原图。
    """
    try:
        path = urlsplit(img_url).path or "/"
    except Exception as err:
        logger.debug(f"每日一言图片地址解析失败 {img_url}: {err}")
        return None

    targets = []
    for edge in _IMAGE_EDGE_HOSTS:
        targets.append((f"http://{edge}{path}{_IMAGE_RESIZE}", _IMAGE_HOST))
        targets.append((f"http://{edge}{path}", _IMAGE_HOST))
    targets.append((f"https://{_IMAGE_HOST}{path}{_IMAGE_RESIZE}", None))
    targets.append((f"https://{_IMAGE_HOST}{path}", None))

    for url, host_header in targets:
        for _ in range(2):
            res = _http_get(url, host_header)
            if res is not None and res.status_code == 200 \
                    and res.content and len(res.content) > 2048:
                return res.content
    return None


class DailyWord(_PluginBase):
    # 插件名称
    plugin_name = "每日一言"
    # 插件描述
    plugin_desc = "在仪表板中显示每日一言卡片。"
    # 插件图标
    plugin_icon = "Calibre_B.png"
    # 插件版本
    #   1.3 netstorm：后端下载图片转 base64（绕过国内七牛节点重置）+ 失败短缓存可重试
    plugin_version = "1.3"
    # 插件作者
    plugin_author = "jxxghp"
    # 作者主页
    author_url = "https://github.com/jxxghp"
    # 插件配置项ID前缀
    plugin_config_prefix = "dailyowrd_"
    # 加载顺序
    plugin_order = 99
    # 可使用的用户级别
    auth_level = 1

    _enable: bool = False
    _size: str = "mini"

    def init_plugin(self, config: dict = None):
        config = config or {}
        self._enable = config.get("enable")
        self._size = config.get("size")

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        pass

    def get_api(self) -> List[Dict[str, Any]]:
        pass

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enable',
                                            'label': '启用插件',
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 4
                                },
                                'content': [
                                    {
                                        'component': 'VSelect',
                                        'props': {
                                            'model': 'size',
                                            'label': '组件规格',
                                            'items': [
                                                {"title": "迷你", "value": "mini"},
                                                {"title": "小型", "value": "small"},
                                                {"title": "中型", "value": "medium"},
                                                {"title": "大型", "value": "large"}
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ], {
            "enable": self._enable,
            "size": self._size
        }

    def get_page(self) -> List[dict]:
        pass

    def get_dashboard_meta(self) -> Optional[List[Dict[str, str]]]:
        """
        获取插件仪表盘元信息
        返回示例：
            [{
                "key": "dashboard1", // 仪表盘的key，在当前插件范围唯一
                "name": "仪表盘1" // 仪表盘的名称
            }, {
                "key": "dashboard2",
                "name": "仪表盘2"
            }]
        """
        return [{
            "key": "dailyword_dashboard",
            "name": "每日一言"
        }]

    def __get_youngam(self, **kwargs) -> Optional[dict]:
        """
        获取每日一言。

        成功缓存 24 小时；失败只缓存 5 分钟 —— 原版用 lru_cache 会把失败
        结果锁死一整天，导致当天再也不会重试。
        """
        today = kwargs.get("today") or datetime.now().strftime("%Y-%m-%d")
        cache_key = f"youngam|{today}"
        cached, hit = _cache_get(cache_key)
        if hit:
            return cached

        result = {}
        try:
            # 1. 获取前十天的图文id数组集合，第一项是今天的图文id
            res = _http_get("http://v3.wufazhuce.com:8000/api/onelist/idlist", timeout=10)
            if res is not None and res.status_code == 200:
                data_list = res.json().get("data") or []
                data_id = data_list[0] if data_list else None
                if data_id:
                    # 2. 根据id获取某一天的图文列表
                    res2 = _http_get(
                        f"http://v3.wufazhuce.com:8000/api/onelist/{data_id}/0", timeout=10)
                    if res2 is not None and res2.status_code == 200:
                        content_list = (res2.json().get("data") or {}).get("content_list") or []
                        content = next(
                            (item for item in content_list if item.get("category") == "0"), None)
                        if content:
                            post_date = content.get("post_date") or ""
                            result = {
                                "src": content.get("img_url"),
                                "text": content.get("forward"),
                                "year": post_date[:4],
                                "month": post_date[5:7],
                                "day": post_date[8:10]
                            }
        except Exception as err:
            logger.error(f"每日一言数据获取失败: {err}")

        if result:
            return _cache_put(cache_key, result, _TTL_OK)
        return _cache_put(cache_key, {}, _TTL_API_FAIL)

    def __image_src(self, today: str, img_url: Optional[str]) -> str:
        """
        把远程图片下载并转成 data URI 内嵌到仪表板 JSON。

        成功：data:image/jpeg;base64,... 缓存 24 小时
        失败：回退 https 原始 URL，只缓存 60 秒 —— 刷新页面即可重试
        """
        if not img_url:
            return ""
        cache_key = f"img|{today}|{img_url}"
        cached, hit = _cache_get(cache_key)
        if hit:
            return cached

        raw = _download_image(img_url)
        if raw:
            src = "data:image/jpeg;base64," + base64.b64encode(raw).decode("utf-8")
            logger.debug(f"每日一言图片已内嵌，{len(raw)} 字节")
            return _cache_put(cache_key, src, _TTL_OK)

        fallback = img_url.replace("http://", "https://", 1)
        logger.warning(f"每日一言图片下载失败，{_TTL_FAIL}s 后可重试：{img_url}")
        return _cache_put(cache_key, fallback, _TTL_FAIL)

    def get_dashboard(self, key: str = None, **kwargs) -> Optional[Tuple[Dict[str, Any], Dict[str, Any], List[dict]]]:
        """
        获取插件仪表盘页面，需要返回：1、仪表板col配置字典；2、全局配置（自动刷新等）；3、仪表板页面元素配置json（含数据）
        1、col配置参考：
        {
            "cols": 12, "md": 6
        }
        2、全局配置参考：
        {
            "refresh": 10 // 自动刷新时间，单位秒
        }
        3、页面配置使用Vuetify组件拼装，参考：https://vuetifyjs.com/
        """
        # 列配置
        if self._size == "mini":
            cols = {
                "cols": 12,
                "md": 4
            }
            height = 160
        elif self._size == "small":
            cols = {
                "cols": 12,
                "md": 6
            }
            height = 262
        elif self._size == "medium":
            cols = {
                "cols": 12,
                "md": 8
            }
            height = 335
        else:
            cols = {
                "cols": 12,
                "md": 12
            }
            height = 500
        # 全局配置
        attrs = {
            "border": False
        }
        # 获取每日一言数据
        today = datetime.now().strftime("%Y-%m-%d")
        data = self.__get_youngam(today=today)
        if not data:
            elements = [
                {
                    'component': 'VCard',
                    'content': [
                        {
                            'component': 'VCardText',
                            'props': {
                                'class': 'text-center',
                            },
                            'content': [
                                {
                                    'component': 'span',
                                    'props': {
                                        'class': 'text-h6'
                                    },
                                    'text': '无数据'
                                }
                            ]
                        }
                    ]
                }
            ]
        else:
            elements = [
                {
                    'component': 'VCard',
                    'props': {
                        'class': 'p-0'
                    },
                    'content': [
                        {
                            'component': 'VImg',
                            'props': {
                                # 后端已转 base64，浏览器不再直连七牛 CDN
                                'src': self.__image_src(today, data.get('src')),
                                'cover': True,
                                'height': height
                            },
                            'content': [
                                {
                                    'component': 'VCardText',
                                    'props': {
                                        'class': 'w-full flex flex-col flex-wrap justify-end align-left text-white absolute bottom-0 pa-4',
                                    },
                                    'content': [
                                        {
                                            'component': 'h1',
                                            'props': {
                                                'class': 'mb-1 text-white text-shadow text-xl line-clamp-4 overflow-hidden text-ellipsis ...'
                                            },
                                            'html': data.get('text'),
                                        },
                                        {
                                            'component': 'span',
                                            'props': {
                                                'class': 'text-right text-shadow line-clamp-2 overflow-hidden text-ellipsis ...'
                                            },
                                            'text': f"{data.get('year')}年{data.get('month')}月{data.get('day')}日",
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }]

        return cols, attrs, elements

    def get_state(self) -> bool:
        return self._enable

    def stop_service(self):
        pass
