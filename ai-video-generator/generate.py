#!/usr/bin/env python3
"""
AI 视频生成器 - 兼容多版本
支持：Agnes AI /v1/video/generations、OpenAI /v1/videos、异步任务轮询格式
"""
import requests
import json
import base64
import os
import sys
import re
import time
import argparse
from datetime import datetime
from pathlib import Path


class VideoGenerator:
    """AI 视频生成器，支持多种 API 格式"""
    
    # 已知的模型配置
    KNOWN_MODELS = {
        # Agnes AI - 使用 /v1/video/generations 端点
        "agnes-video": {"api_type": "agnes", "default_seconds": 5, "default_size": "720x1280"},
        # OpenAI Sora
        "sora": {"api_type": "videos", "default_seconds": 8, "default_size": "1280x720"},
        # Google Veo
        "veo": {"api_type": "videos", "default_seconds": 8, "default_size": "1280x720"},
        # 可灵
        "kling": {"api_type": "async", "default_seconds": 5, "default_size": "1280x720"},
        # 混元
        "hunyuan": {"api_type": "async", "default_seconds": 5, "default_size": "1280x720"},
        # 通义万相
        "wanx": {"api_type": "async", "default_seconds": 4, "default_size": "1280x720"},
    }
    
    def __init__(self, config):
        """
        初始化视频生成器
        
        Args:
            config: 配置字典，包含 api_key, base_url, model, api_type
        """
        self.api_key = config.get("api_key", "")
        self.base_url = config.get("base_url", "https://api.openai.com/v1").rstrip("/")
        self.model = config.get("model", "sora-2")
        self.api_type = config.get("api_type", "auto")
        self.timeout = config.get("timeout", 300)
        
        if not self.api_key:
            raise ValueError("API Key 不能为空，请在配置文件中设置 api_key")
    
    def generate(self, prompt, seconds=None, size=None, output_path=None, image=None, 
                 poll_interval=5, max_wait=600, **kwargs):
        """
        生成视频
        
        Args:
            prompt: 视频描述
            seconds: 视频时长（秒）
            size: 视频尺寸
            output_path: 输出路径
            image: 参考图片路径（图生视频）
            poll_interval: 轮询间隔（秒）
            max_wait: 最大等待时间（秒）
            
        Returns:
            成功返回视频文件路径，失败返回 None
        """
        # 设置默认值
        model_config = self._get_model_config()
        if seconds is None:
            seconds = model_config.get("default_seconds", 8)
        if size is None:
            size = model_config.get("default_size", "1280x720")
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/workspace/video_{timestamp}.mp4"
        
        api_type = self._detect_api_type()
        
        print(f"[VideoGen] Prompt: {prompt}")
        print(f"[VideoGen] 模型: {self.model} | API: {api_type}")
        print(f"[VideoGen] 时长: {seconds}s | 尺寸: {size}")
        
        try:
            if api_type == "agnes":
                return self._gen_agnes(prompt, seconds, size, output_path, poll_interval, max_wait)
            elif api_type == "videos":
                return self._gen_videos(prompt, seconds, size, output_path, poll_interval, max_wait)
            elif api_type == "chat":
                return self._gen_chat(prompt, seconds, size, output_path, image)
            elif api_type == "async":
                return self._gen_async(prompt, seconds, size, output_path, poll_interval, max_wait)
            else:
                # 自动尝试多种方式
                result = self._gen_agnes(prompt, seconds, size, output_path, poll_interval, max_wait)
                if result:
                    return result
                result = self._gen_videos(prompt, seconds, size, output_path, poll_interval, max_wait)
                if result:
                    return result
                return self._gen_chat(prompt, seconds, size, output_path, image)
        except Exception as e:
            print(f"[VideoGen] 生成失败: {e}")
            return None
    
    def _get_model_config(self):
        """获取模型配置"""
        model_lower = self.model.lower()
        for key, config in self.KNOWN_MODELS.items():
            if key in model_lower:
                return config
        return {}
    
    def _detect_api_type(self):
        """检测 API 类型"""
        if self.api_type != "auto":
            return self.api_type
        
        # 根据模型名自动检测
        model_config = self._get_model_config()
        if model_config.get("api_type"):
            return model_config["api_type"]
        
        # 默认尝试 agnes 格式
        return "agnes"
    
    def _get_headers(self):
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _gen_agnes(self, prompt, seconds, size, output_path, poll_interval, max_wait):
        """
        Agnes AI 视频生成
        端点: POST /v1/video/generations
        状态: GET /v1/videos/{task_id}
        """
        url = f"{self.base_url}/video/generations"
        headers = self._get_headers()
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "n": 1
        }
        
        try:
            # 提交任务
            print(f"[VideoGen] 提交视频生成任务到 Agnes AI...")
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            
            task_id = result.get("task_id") or result.get("id")
            status = result.get("status", "queued")
            
            if not task_id:
                print(f"[VideoGen] 未获取到任务ID，尝试直接提取视频...")
                return self._extract_video(result, output_path)
            
            print(f"[VideoGen] 任务已提交: {task_id}")
            
            # 轮询状态
            return self._poll_agnes_status(
                task_id, status, output_path, poll_interval, max_wait
            )
            
        except requests.exceptions.HTTPError as e:
            print(f"[VideoGen] HTTP 错误: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[VideoGen] 响应: {e.response.text[:500]}")
            return None
        except Exception as e:
            print(f"[VideoGen] 请求失败: {e}")
            return None
    
    def _poll_agnes_status(self, task_id, initial_status, output_path, poll_interval, max_wait):
        """轮询 Agnes AI 任务状态"""
        headers = self._get_headers()
        status_url = f"{self.base_url}/videos/{task_id}"
        
        start_time = time.time()
        status = initial_status
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > max_wait:
                print(f"[VideoGen] 超时（已等待 {int(elapsed)}s）")
                return None
            
            print(f"[VideoGen] 状态: {status} | 进度: {int((time.time() - start_time) / max_wait * 100)}% ({int(elapsed)}s)")
            
            if status in ["completed", "succeed", "success", "done"]:
                # 从响应中提取视频 URL
                return self._download_from_remix_url(output_path)
            elif status in ["failed", "error", "cancelled"]:
                print(f"[VideoGen] 任务失败: {status}")
                return None
            
            time.sleep(poll_interval)
            
            try:
                resp = requests.get(status_url, headers=headers, timeout=30)
                resp.raise_for_status()
                result = resp.json()
                status = result.get("status", status)
                
                # 保存完整的响应以便调试
                if status in ["completed", "succeed", "success", "done"]:
                    self._last_result = result
                    return self._download_from_remix_url(output_path)
                    
            except Exception as e:
                print(f"[VideoGen] 轮询失败: {e}")
    
    def _download_from_remix_url(self, output_path):
        """从 remixed_from_video_id 下载视频"""
        if hasattr(self, '_last_result') and self._last_result:
            video_url = self._last_result.get("remixed_from_video_id")
            if video_url:
                return self._download_from_url(video_url, output_path)
        
        print("[VideoGen] 未找到视频下载链接")
        return None
    
    def _gen_videos(self, prompt, seconds, size, output_path, poll_interval, max_wait):
        """
        使用 /v1/videos 端点生成视频（OpenAI 格式）
        """
        url = f"{self.base_url}/videos"
        headers = self._get_headers()
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "seconds": str(seconds),
            "size": size
        }
        
        try:
            # 提交任务
            print(f"[VideoGen] 提交视频生成任务...")
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            
            video_id = result.get("id") or result.get("video_id") or result.get("task_id")
            status = result.get("status", "pending")
            
            if not video_id:
                # 可能直接返回了视频 URL
                return self._extract_video(result, output_path)
            
            print(f"[VideoGen] 任务已提交: {video_id}")
            
            # 轮询状态
            return self._poll_video_status(
                video_id, status, output_path, poll_interval, max_wait
            )
            
        except requests.exceptions.HTTPError as e:
            print(f"[VideoGen] HTTP 错误: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[VideoGen] 响应: {e.response.text[:500]}")
            return None
        except Exception as e:
            print(f"[VideoGen] 请求失败: {e}")
            return None
    
    def _poll_video_status(self, video_id, initial_status, output_path, poll_interval, max_wait):
        """轮询视频生成状态"""
        headers = self._get_headers()
        status_url = f"{self.base_url}/videos/{video_id}"
        content_url = f"{self.base_url}/videos/{video_id}/content"
        
        start_time = time.time()
        status = initial_status
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > max_wait:
                print(f"[VideoGen] 超时（已等待 {int(elapsed)}s）")
                return None
            
            print(f"[VideoGen] 状态: {status} ({int(elapsed)}s)")
            
            if status in ["completed", "succeed", "success", "done"]:
                # 下载视频
                return self._download_video(content_url, headers, output_path)
            elif status in ["failed", "error", "cancelled"]:
                print(f"[VideoGen] 任务失败: {status}")
                return None
            
            time.sleep(poll_interval)
            
            try:
                resp = requests.get(status_url, headers=headers, timeout=30)
                resp.raise_for_status()
                result = resp.json()
                status = result.get("status", status)
                
                # 检查是否有视频 URL
                if result.get("video_url") or result.get("url"):
                    return self._extract_video(result, output_path)
                    
            except Exception as e:
                print(f"[VideoGen] 轮询失败: {e}")
    
    def _download_video(self, content_url, headers, output_path):
        """下载视频文件"""
        try:
            print(f"[VideoGen] 下载视频...")
            resp = requests.get(content_url, headers=headers, timeout=120, stream=True)
            resp.raise_for_status()
            
            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(output_path)
            print(f"[VideoGen] 已保存: {output_path} ({file_size / 1024 / 1024:.2f} MB)")
            return output_path
            
        except Exception as e:
            print(f"[VideoGen] 下载失败: {e}")
            return None
    
    def _extract_video(self, result, output_path):
        """从响应中提取视频"""
        # 检查 data 数组
        if "data" in result and result["data"]:
            item = result["data"][0] if isinstance(result["data"], list) else result["data"]
            if item.get("url") or item.get("video_url"):
                video_url = item.get("url") or item.get("video_url")
                return self._download_from_url(video_url, output_path)
        
        # 直接检查顶层 URL
        for key in ["url", "video_url", "video_content_url", "remixed_from_video_id"]:
            if result.get(key):
                return self._download_from_url(result[key], output_path)
        
        # 保存 JSON 响应
        json_path = output_path.replace(".mp4", ".json")
        with open(json_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"[VideoGen] 响应已保存: {json_path}")
        return json_path
    
    def _download_from_url(self, url, output_path):
        """从 URL 下载视频"""
        try:
            print(f"[VideoGen] 下载: {url[:80]}...")
            resp = requests.get(url, timeout=120, stream=True)
            resp.raise_for_status()
            
            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(output_path)
            print(f"[VideoGen] 已保存: {output_path} ({file_size / 1024 / 1024:.2f} MB)")
            return output_path
            
        except Exception as e:
            print(f"[VideoGen] 下载失败: {e}")
            return None
    
    def _gen_chat(self, prompt, seconds, size, output_path, image=None):
        """
        使用 /v1/chat/completions 端点生成视频
        """
        url = f"{self.base_url}/chat/completions"
        headers = self._get_headers()
        
        # 构建消息内容
        content = self._build_chat_content(prompt, seconds, size, image)
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": content}
            ],
            "stream": False
        }
        
        try:
            print(f"[VideoGen] 通过 Chat API 生成视频...")
            resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            result = resp.json()
            
            # 提取响应内容
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # 尝试从内容中提取视频
            return self._extract_from_chat_content(content, output_path)
            
        except requests.exceptions.HTTPError as e:
            print(f"[VideoGen] HTTP 错误: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[VideoGen] 响应: {e.response.text[:500]}")
            return None
        except Exception as e:
            print(f"[VideoGen] 请求失败: {e}")
            return None
    
    def _build_chat_content(self, prompt, seconds, size, image=None):
        """构建聊天消息内容"""
        # 如果有参考图片
        if image and os.path.exists(image):
            with open(image, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
            
            ext = Path(image).suffix.lower().lstrip(".")
            if ext in ["jpg", "jpeg"]:
                ext = "jpeg"
            
            return [
                {
                    "type": "text",
                    "text": f"请根据这张图片生成视频：{prompt}，时长 {seconds} 秒"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{ext};base64,{image_data}"
                    }
                }
            ]
        
        # 纯文本
        return f"生成视频：{prompt}，时长 {seconds} 秒，尺寸 {size}"
    
    def _extract_from_chat_content(self, content, output_path):
        """从聊天响应内容中提取视频"""
        if not content:
            print("[VideoGen] 响应内容为空")
            return None
        
        # 尝试提取 base64 视频
        video_match = re.search(r'data:video/\w+;base64,([A-Za-z0-9+/=]+)', content)
        if video_match:
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(video_match.group(1)))
            print(f"[VideoGen] 已保存: {output_path}")
            return output_path
        
        # 尝试提取视频 URL
        url_match = re.search(r'(https?://[^\s\'"]+\.(?:mp4|mov|avi|webm|mkv))', content, re.IGNORECASE)
        if url_match:
            return self._download_from_url(url_match.group(1), output_path)
        
        # 尝试提取通用 URL
        url_match = re.search(r'(https?://[^\s\'"]+)', content)
        if url_match:
            url = url_match.group(1)
            if any(keyword in url.lower() for keyword in ["video", "download", "content"]):
                return self._download_from_url(url, output_path)
        
        # 保存文本响应
        txt_path = output_path.replace(".mp4", ".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[VideoGen] 文本响应已保存: {txt_path}")
        
        # 也保存 JSON
        json_path = output_path.replace(".mp4", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({"content": content}, f, indent=2, ensure_ascii=False)
        
        return txt_path
    
    def _gen_async(self, prompt, seconds, size, output_path, poll_interval, max_wait):
        """
        异步任务模式生成视频
        """
        headers = self._get_headers()
        
        # 提交任务
        submit_url = f"{self.base_url}/videos/generations"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "n": 1,
            "seconds": seconds,
            "size": size
        }
        
        try:
            print(f"[VideoGen] 提交异步任务...")
            resp = requests.post(submit_url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            
            task_id = result.get("id") or result.get("task_id")
            if not task_id:
                return self._extract_video(result, output_path)
            
            print(f"[VideoGen] 任务已提交: {task_id}")
            
            # 轮询任务状态
            start_time = time.time()
            while True:
                elapsed = time.time() - start_time
                if elapsed > max_wait:
                    print(f"[VideoGen] 超时")
                    return None
                
                time.sleep(poll_interval)
                
                # 尝试不同的轮询端点
                poll_urls = [
                    f"{self.base_url}/videos/tasks/{task_id}",
                    f"{self.base_url}/videos/{task_id}",
                    f"{self.base_url}/tasks/{task_id}",
                ]
                
                for poll_url in poll_urls:
                    try:
                        resp = requests.get(poll_url, headers=headers, timeout=30)
                        if resp.status_code == 200:
                            result = resp.json()
                            status = result.get("status", "")
                            
                            print(f"[VideoGen] 状态: {status} ({int(elapsed)}s)")
                            
                            if status in ["succeed", "completed", "success", "done"]:
                                return self._extract_video(result, output_path)
                            elif status in ["failed", "error"]:
                                return None
                            
                            break
                    except:
                        continue
                        
        except Exception as e:
            print(f"[VideoGen] 异步任务失败: {e}")
            return None
    
    def get_status(self, task_id):
        """
        查询任务状态
        
        Args:
            task_id: 任务 ID
            
        Returns:
            状态信息字典
        """
        headers = self._get_headers()
        
        poll_urls = [
            f"{self.base_url}/videos/{task_id}",
            f"{self.base_url}/videos/tasks/{task_id}",
            f"{self.base_url}/tasks/{task_id}",
        ]
        
        for url in poll_urls:
            try:
                resp = requests.get(url, headers=headers, timeout=30)
                if resp.status_code == 200:
                    return resp.json()
            except:
                continue
        
        return {"status": "unknown", "error": "无法获取状态"}


def main():
    parser = argparse.ArgumentParser(description="AI 视频生成器")
    parser.add_argument("prompt", nargs="?", help="视频描述")
    parser.add_argument("--seconds", "-s", type=int, default=None, help="视频时长（秒）")
    parser.add_argument("--size", default=None, help="视频尺寸 (1280x720, 720x1280)")
    parser.add_argument("--output", "-o", default=None, help="输出路径")
    parser.add_argument("--image", "-i", default=None, help="参考图片路径（图生视频）")
    parser.add_argument("--config", "-c", default="/workspace/video_api_config.json", help="配置文件路径")
    parser.add_argument("--poll-interval", type=int, default=5, help="轮询间隔（秒）")
    parser.add_argument("--max-wait", type=int, default=600, help="最大等待时间（秒）")
    parser.add_argument("--status", default=None, help="查询任务状态")
    parser.add_argument("--list-models", action="store_true", help="列出已知模型")
    
    args = parser.parse_args()
    
    # 列出已知模型
    if args.list_models:
        print("已知视频生成模型:")
        for model, config in VideoGenerator.KNOWN_MODELS.items():
            print(f"  - {model}: API={config['api_type']}, 默认时长={config['default_seconds']}s")
        return
    
    # 加载配置
    if not os.path.exists(args.config):
        print(f"错误: 配置文件不存在: {args.config}")
        print("请创建配置文件，示例:")
        print(json.dumps({
            "api_key": "your-api-key",
            "base_url": "https://apihub.agnes-ai.com/v1",
            "model": "agnes-video-v2.0",
            "api_type": "auto"
        }, indent=2))
        sys.exit(1)
    
    with open(args.config) as f:
        config = json.load(f)
    
    generator = VideoGenerator(config)
    
    # 查询状态
    if args.status:
        result = generator.get_status(args.status)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    
    # 生成视频
    if not args.prompt:
        parser.print_help()
        sys.exit(1)
    
    result = generator.generate(
        prompt=args.prompt,
        seconds=args.seconds,
        size=args.size,
        output_path=args.output,
        image=args.image,
        poll_interval=args.poll_interval,
        max_wait=args.max_wait
    )
    
    if result:
        print(f"\n✅ 视频生成成功！")
        print(f"📁 文件路径: {result}")
    else:
        print(f"\n❌ 视频生成失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
