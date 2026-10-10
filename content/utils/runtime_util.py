from langchain_core.runnables.config import var_child_runnable_config as vcrc
from base import config
import os
# thread_id 通常存储在 configurable 字段中
def get_thread_id():
    # 当你的Agent在处理用户请求时，框架会在后台维护一个“上下文变量”（ContextVariable）。var_child_runnable_config（我们简称为
    # vcrc就是这个上下文变量的名字。你可以把它想象成一个隐形的全局背包，LangGraph
    # 在调用你的
    # Agent
    # 时，会自动把当前的配置（包含
    # thread_id）塞进这个背包里。
    config = vcrc.get()
    if config: # 配置不为空
        configurable = config.get('configurable')
        if configurable: # 配置不为空
            return configurable.get('thread_id','default') # 返回 thread_id
    return "default" # 返回默认值

def get_thread_dir():
# 用户 A 正在和 Agent 聊天，get_thread_id() 返回了 "user_A_session_123"。
# 当 Agent 需要读写文件时，调用 get_thread_dir()，它会返回：/data/my_agent/user_A_session_123。
    #os.path.normpath 是规划化路径的操作，重点就是'/'规划一下
    return os.path.normpath(os.path.join(config.ROOT_PATH_AGENT, get_thread_id()))


def change_file_path(path):
    """
       转换文件路径为当前线程对应的文件路径
        # 例如：/user_upload/a.txt -> /agent_files/[thread_id]/a.txt
       Args:
           file_path: 原始文件路径
       Returns:
           str: 转换后的文件路径
           强制把 LLM 或用户提供的任意文件路径，重定向并锁定到当前对话专属的“办公房间”里。
    """
    # 提示：会用到这两个函数
    root_dir = get_thread_dir()
    path = os.path.normpath(path) # 规范化这个路径本身
    if root_dir in path: # 如果路径本身就包含了根目录，则直接返回
        return path
    if os.path.isabs( path): # 判断路径是否是绝对路径
        path = os.path.relpath(path, start='/') # 获取相对路径
    return os.path.normpath(os.path.join(root_dir, path)) # 与真正的工作目录路径拼接


def get_out_path(text):
    if not isinstance(text, str):return text
    # text = 'python /agent_files/aasdsada/a.py'
    # -> = 'python /a.py'
    # 先得到线程路径
    thread_dir = get_thread_dir()
    # 把text中存在的线程路径删除掉
    text = os.path.normpath(text)
    text = text.replace(thread_dir, '')
    return text

if __name__ == "__main__":
    text = 'python /asda/a.py'
    print(os.path.normpath(text))
    #print(get_out_path(text))