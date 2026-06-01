"""
自定义中间件模块
Custom middleware module
"""


class NoCacheMiddleware:
    """
    禁止浏览器缓存认证页面的中间件
    Prevent browser from caching authenticated pages

    对 HTML 页面响应添加 Cache-Control 头部，确保：
    - 浏览器不会缓存任何 HTML 页面到 disk/memory cache
    - 登出后使用前进/后退按钮不会回显已登录页面
    - 浏览器始终从服务器重新请求页面以验证认证状态
    - 静态文件（CSS/JS/图片）的缓存不受影响
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        content_type = response.get('Content-Type', '')
        if 'text/html' in content_type:
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response
