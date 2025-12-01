import os
import requests
from urllib.parse import urljoin

# === 配置部分 ===

VERSION = "8.39.2"
BASE_URL = f"https://ssl.p.jwpcdn.com/player/v/{VERSION}/"
OUTPUT_DIR = f"jwplayer/{VERSION}"


# a = """""".strip().split("\n")
# a = [f'"{i}",\n' for i in a]
# print(''.join(a))


FILES_TO_DOWNLOAD = [
    "dai.js",  # 动态广告插入
    "freewheel.js",  # FreeWheel 广告支持
    "gapro.js",  # Google Analytics Pro
    "googima.js",  # Google IMA 广告 SDK
    "jwplayer.controls.js",  # 控制栏 UI
    "jwplayer.core.controls.html5.js",  # HTML5 核心控制
    "jwplayer.core.controls.js",  # 通用核心控制
    "jwplayer.core.controls.polyfills.html5.js",  # HTML5 兼容补丁
    "jwplayer.core.controls.polyfills.js",  # 通用兼容补丁
    "jwplayer.core.js",  # 播放器内核
    "jwplayer.flash.swf",  # Flash 播放器文件 (旧浏览器用)
    "jwplayer.js",  # 主引导文件
    "jwplayer.vr.js",  # VR/360视频支持
    "jwpsrv.js",  # 统计与服务回报
    "notice.txt",  # 版权声明
    "polyfills.intersection-observer.js",  # 视口检测兼容库
    "polyfills.webvtt.js",  # 字幕解析兼容库
    "provider.airplay.js",  # Apple AirPlay 支持
    "provider.cast.js",  # Google Chromecast 支持
    "provider.flash.js",  # Flash 提供程序
    "provider.hlsjs.js",  # HLS 流媒体核心
    "provider.hlsjs-progressive.js",  # HLS 渐进式下载支持
    "provider.html5.js",  # 标准 MP4/WebM 支持
    "provider.shaka.js",  # DASH 流媒体 (Shaka Player)
    "related.js",  # 推荐视频模块
    "vast.js",  # VAST 广告标准支持
    "vttparser.js",  # WebVTT 字幕解析器

    "interactive.js",                           # 交互式视频功能
    "jwplayer.amp.js",                          # Google AMP 页面支持
    "jwplayer.compatibility.js",                # 额外兼容性补丁
    "jwplayer.controls.tizen.js",               # 三星 Tizen TV 专用皮肤
    "jwplayer.stats.js",                        # 播放器统计模块
    "jwpsrv-dnt.js",                            # 隐私模式(Do Not Track)统计服务


    # --- 多语言文件 (Translations) ---
    "translations/ar.json",
    "translations/da.json",
    "translations/de.json",
    "translations/es.json",
    "translations/fi.json",
    "translations/fr.json",
    "translations/he.json",
    "translations/id.json",
    "translations/it.json",
    "translations/ja.json",
    "translations/ko.json",
    "translations/nl.json",
    "translations/no.json",
    "translations/oc.json",
    "translations/pt.json",
    "translations/ro.json",
    "translations/ru.json",
    "translations/sl.json",
    "translations/sv.json",
    "translations/th.json",
    "translations/tr.json",
    "translations/vi.json",
    "translations/zh.json",
]


# === 核心逻辑 ===

def download_files():
    # 创建主目录
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"创建目录: {OUTPUT_DIR}")

    print(f"开始从 {BASE_URL} 下载文件...\n")

    success_count = 0
    fail_count = 0

    for file_path in FILES_TO_DOWNLOAD:
        # 拼接完整的下载链接
        url = urljoin(BASE_URL, file_path)

        # 拼接本地保存路径 (处理子文件夹，如 translations/zh.json)
        local_path = os.path.join(OUTPUT_DIR, file_path.replace("/", os.sep))
        local_dir = os.path.dirname(local_path)

        # 如果子文件夹不存在，则创建
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        try:
            print(f"正在下载: {file_path} ...", end="\r")

            # 发起请求
            response = requests.get(url, stream=True, timeout=10)

            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"[成功] {file_path}            ")
                success_count += 1
            elif response.status_code == 404:
                print(f"[跳过] {file_path} (服务器上不存在)")
                # 有些文件不是必须的，404 属于正常现象
                fail_count += 1
            else:
                print(f"[失败] {file_path} (状态码: {response.status_code})")
                fail_count += 1

        except Exception as e:
            print(f"[错误] {file_path}: {str(e)}")
            fail_count += 1

    print("\n" + "=" * 30)
    print(f"下载完成。成功: {success_count}, 未找到/失败: {fail_count}")
    print(f"文件保存在: {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    download_files()
