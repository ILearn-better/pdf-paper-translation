from logger import logger
def print_and_logger(step,postion,message):
    """
    参数:
    step:当前所处流程
    position:程序执行路径
    message:消息
    :return:
    """
    print("流程:{},地址:{},信息:{}".format(step,postion,message))
    logger.info("流程:{},地址:{},信息:{}".format(step,postion,message))
