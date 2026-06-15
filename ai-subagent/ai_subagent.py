#!/usr/bin/env python3
"""
真正 AI 子 Agent 系统
每个子 Agent 都有独立的 AI 推理能力
"""
import threading
import time
import json
import requests
from queue import Queue
from datetime import datetime

class AISubAgent:
    """单个 AI 子 Agent"""
    
    def __init__(self, agent_id, config):
        self.agent_id = agent_id
        self.config = config
        self.history = []  # 独立对话历史
        self.name = config.get("name", f"Agent-{agent_id}")
        self.model = config.get("model", "deepseek-chat")
    
    def chat(self, message):
        """发送消息给 AI，获取回复"""
        self.history.append({"role": "user", "content": message})
        
        url = self.config.get("url", "https://api.deepseek.com/chat/completions")
        api_key = self.config.get("api_key", "")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": self.history,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            self.history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"API 调用失败: {str(e)}"
    
    def execute_task(self, task):
        """执行任务"""
        print(f"[{self.name}] 开始执行: {task.get('desc', '任务')}")
        start_time = time.time()
        
        try:
            # 构建 prompt
            system_prompt = task.get("system_prompt", "你是一个专业的 AI 助手。")
            user_prompt = task.get("prompt", "")
            
            # 先设置角色
            if system_prompt:
                self.chat(system_prompt)
            
            # 执行任务
            result = self.chat(user_prompt)
            elapsed = time.time() - start_time
            
            return {
                "agent_id": self.agent_id,
                "name": self.name,
                "status": "success",
                "result": result,
                "elapsed": round(elapsed, 2),
                "desc": task.get("desc", "任务")
            }
        except Exception as e:
            elapsed = time.time() - start_time
            return {
                "agent_id": self.agent_id,
                "name": self.name,
                "status": "error",
                "error": str(e),
                "elapsed": round(elapsed, 2),
                "desc": task.get("desc", "任务")
            }

class AISubAgentSystem:
    """AI 子 Agent 系统"""
    
    def __init__(self, config):
        """
        config = {
            "api_key": "your-api-key",
            "url": "https://api.deepseek.com/chat/completions",
            "model": "deepseek-chat"
        }
        """
        self.config = config
        self.agents = []
        self.results = []
    
    def create_agent(self, name=None):
        """创建子 Agent"""
        agent_id = len(self.agents)
        agent_config = self.config.copy()
        if name:
            agent_config["name"] = name
        agent = AISubAgent(agent_id, agent_config)
        self.agents.append(agent)
        return agent
    
    def run_parallel(self, tasks):
        """
        并行执行任务
        tasks = [
            {"desc": "任务1", "prompt": "...", "system_prompt": "..."},
            {"desc": "任务2", "prompt": "...", "system_prompt": "..."},
        ]
        """
        print(f"=== 启动 {len(tasks)} 个 AI 子 Agent ===")
        start_time = time.time()
        
        result_queue = Queue()
        threads = []
        
        for i, task in enumerate(tasks):
            agent = self.create_agent(task.get("name"))
            
            def worker(agent, task, queue):
                result = agent.execute_task(task)
                queue.put(result)
            
            t = threading.Thread(target=worker, args=(agent, task, result_queue))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        while not result_queue.empty():
            self.results.append(result_queue.get())
        
        self.results.sort(key=lambda x: x["agent_id"])
        
        total_time = time.time() - start_time
        print(f"=== 所有 AI Agent 完成，总耗时: {round(total_time, 2)}s ===")
        
        return self.results
    
    def print_results(self):
        """打印结果"""
        print("\n=== AI 子 Agent 结果汇总 ===")
        for r in self.results:
            status = "成功" if r["status"] == "success" else "失败"
            print(f"\n[{r['name']}] {r['desc']} - {status} ({r['elapsed']}s)")
            if r["status"] == "success":
                print(f"回复: {r['result'][:200]}...")
            else:
                print(f"错误: {r['error']}")
    
    def get_summary(self):
        """获取汇总"""
        success = sum(1 for r in self.results if r["status"] == "success")
        failed = sum(1 for r in self.results if r["status"] == "error")
        total_time = sum(r["elapsed"] for r in self.results)
        
        return {
            "total": len(self.results),
            "success": success,
            "failed": failed,
            "total_time": round(total_time, 2),
            "results": self.results
        }

# 配置模板
CONFIG_TEMPLATE = {
    "api_key": "YOUR_API_KEY_HERE",  # 替换成你的 API Key
    "url": "https://api.deepseek.com/chat/completions",  # API 地址
    "model": "deepseek-chat"  # 模型名称
}

if __name__ == "__main__":
    print("=== AI 子 Agent 系统 ===")
    print("\n使用前请配置 API Key:")
    print("1. 编辑 CONFIG_TEMPLATE 中的 api_key")
    print("2. 或者运行时传入 config")
    
    # 示例（需要 API Key 才能运行）
    # config = {
    #     "api_key": "your-api-key",
    #     "url": "https://api.deepseek.com/chat/completions",
    #     "model": "deepseek-chat"
    # }
    # system = AISubAgentSystem(config)
    # tasks = [
    #     {"desc": "搜索分析", "prompt": "分析 Python 的优势", "system_prompt": "你是一个技术分析师"},
    #     {"desc": "内容生成", "prompt": "写一段关于 AI 的介绍", "system_prompt": "你是一个内容创作者"},
    # ]
    # results = system.run_parallel(tasks)
    # system.print_results()