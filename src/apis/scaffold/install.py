# -*- coding: utf-8 -*-
# Time       : 2022/1/20 16:16
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import sys
import webbrowser
from typing import Optional

from webdriver_manager.chrome import ChromeType
from webdriver_manager.utils import get_browser_version_from_os

from services.settings import DIR_MODEL, logger, PATH_OBJECTS_YAML, DIR_ASSETS
from services.utils import YOLO, PluggableONNXModels, get_challenge_ctx
from services.utils.armor.anti_hcaptcha.solutions.kernel import Rainbow


def download_driver():
    # Detect environment variable `google-chrome`.
    browser_version = get_browser_version_from_os(ChromeType.GOOGLE)
    if browser_version != "UNKNOWN":
        return

    # `google-chrome` is missing from environment variables, prompting players to install manually.
    logger.critical(
        "The current environment variable is missing `google-chrome`, "
        "please install Chrome for your system"
    )
    logger.info(
        "Ubuntu: https://linuxize.com/post/how-to-install-google-chrome-web-browser-on-ubuntu-20-04/"
    )
    logger.info(
        "CentOS 7/8: https://linuxize.com/post/how-to-install-google-chrome-web-browser-on-centos-7/"
    )
    if "linux" not in sys.platform:
        webbrowser.open("https://www.google.com/chrome/")

    logger.info("Re-execute the `install` scaffolding command after the installation is complete.")


def do(yolo_onnx_prefix: Optional[str] = None, upgrade: Optional[bool] = False):
    """下载项目运行所需的各项依赖"""
    download_driver()

    # PULL rainbow table
    Rainbow(DIR_ASSETS).sync()

    # PULL YOLO ONNX Model by the prefix flag
    YOLO(DIR_MODEL, yolo_onnx_prefix).pull_model()

    # PULL ResNet ONNX Model(s) by objects.yaml
    if upgrade is True:
        PluggableONNXModels(PATH_OBJECTS_YAML).summon(DIR_MODEL)


@logger.catch()
def test():
    """Check if the Challenger driver version is compatible"""
    ctx = get_challenge_ctx(silence=True)
    try:
        ctx.get("https://blog.echosec.top/p/spider_performance/")
    finally:
        ctx.quit()

    logger.success("The adaptation is successful")
