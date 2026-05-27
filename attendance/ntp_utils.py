"""
NTP 时间同步工具模块
使用 ntplib 从阿里云 NTP 服务器获取网络时间，确保系统时间准确一致
所有时间判断逻辑（签到码过期校验、签到时间记录、迟到判定等）均以 NTP 时间为准
"""
import ntplib
from datetime import datetime, timezone
import logging

logger = logging.getLogger('audit')

# NTP 服务器地址
# NTP server address
NTP_SERVER = 'ntp.aliyun.com'


def get_ntp_time():
    """
    从 NTP 服务器获取当前网络时间
    返回一个 timezone-aware datetime 对象（UTC 时区）
    如果获取失败，返回 None
    """
    try:
        client = ntplib.NTPClient()
        response = client.request(NTP_SERVER, version=3, timeout=5)
        # NTP 时间戳转换为 datetime
        # Convert NTP timestamp to datetime
        ntp_timestamp = response.tx_time
        utc_time = datetime.fromtimestamp(ntp_timestamp, tz=timezone.utc)
        return utc_time
    except Exception as e:
        logger.warning(f'NTP 时间获取失败，将使用本地系统时间：{e}')
        return None


def get_current_time():
    """
    获取当前时间（优先使用 NTP 时间，失败则使用本地系统时间）
    返回 timezone-aware datetime 对象
    """
    ntp_time = get_ntp_time()
    if ntp_time:
        return ntp_time
    # NTP 不可用时降级使用本地系统时间
    # Fallback to local system time if NTP unavailable
    return datetime.now(tz=timezone.utc)
