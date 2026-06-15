#!/usr/bin/env python3
"""
AI 图片生成器 - 兼容多版本
支持：OpenAI 格式、Chat Completion 格式、异步任务格式
"""
import requests
import json
import base64
import os
import sys
import re
import time
from datetime import datetime


class ImageGenerator:
    def __init__(self, config):
        self.api_key = config.get("api_key", "")
        self.base_url = config.get("base_url", "https://api.openai.com/v1")
        self.model = config.get("model", "dall-e-3")
        self.api_type = config.get("api_type", "auto")
    
    def generate(self, prompt, size="1024x1024", output_path=None):
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/workspace/generated_{timestamp}.png"
        
        api_type = self._detect_api_type()
        print(f"[ImageGen] Prompt: {prompt}")
        print(f"[ImageGen] 模型: {self.model} | API: {api_type}")
        
        if api_type == "images":
            return self._gen_images(prompt, size, output_path)
        elif api_type == "chat":
            return self._gen_chat(prompt, output_path)
        elif api_type == "async":
            return self._gen_async(prompt, size, output_path)
        else:
            result = self._gen_images(prompt, size, output_path)
            return result if result else self._gen_chat(prompt, output_path)
    
    def _detect_api_type(self):
        if self.api_type != "auto":
            return self.api_type
        chat_models = ["nano-banana", "gpt-image-2"]
        async_models = ["kling", "hy-image"]
        m = self.model.lower()
        for x in chat_models:
            if x in m: return "chat"
        for x in async_models:
            if x in m: return "async"
        return "images"
    
    def _gen_images(self, prompt, size, output_path):
        url = f"{self.base_url}/images/generations"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "prompt": prompt, "n": 1, "size": size}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
            return self._extract(resp.json(), output_path)
        except Exception as e:
            print(f"[ImageGen] 失败: {e}")
            return None
    
    def _gen_chat(self, prompt, output_path):
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": [{"role": "user", "content": f"生成图片: {prompt}"}]}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            match = re.search(r'data:image/\w+;base64,([A-Za-z0-9+/=]+)', content)
            if match:
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(match.group(1)))
                return output_path
            url_match = re.search(r'(https?://[^\s\'"]+\.(?:png|jpg|jpeg|webp))', content)
            if url_match:
                img = requests.get(url_match.group(1), timeout=60)
                with open(output_path, "wb") as f:
                    f.write(img.content)
                return output_path
            txt_path = output_path.replace(".png", ".txt")
            with open(txt_path, "w") as f:
                f.write(content)
            return txt_path
        except Exception as e:
            print(f"[ImageGen] 失败: {e}")
            return None
    
    def _gen_async(self, prompt, size, output_path):
        url = f"{self.base_url}/images/generations"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "prompt": prompt, "n": 1, "size": size}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            task_id = result.get("id") or result.get("task_id")
            if not task_id:
                return self._extract(result, output_path)
            print(f"[ImageGen] 任务ID: {task_id}")
            for i in range(60):
                time.sleep(5)
                poll = requests.get(f"{self.base_url}/images/tasks/{task_id}", headers=headers, timeout=30).json()
                if poll.get("status") in ["succeed", "completed"]:
                    return self._extract(poll, output_path)
                elif poll.get("status") == "failed":
                    return None
                print(f"[ImageGen] {poll.get('status')} ({i*5}s)")
            return None
        except Exception as e:
            print(f"[ImageGen] 失败: {e}")
            return None
    
    def _extract(self, result, output_path):
        if "data" in result and result["data"]:
            item = result["data"][0]
            if item.get("url"):
                img = requests.get(item["url"], timeout=60)
                with open(output_path, "wb") as f:
                    f.write(img.content)
                print(f"[ImageGen] 已保存: {output_path}")
                return output_path
            if item.get("b64_json"):
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(item["b64_json"]))
                print(f"[ImageGen] 已保存: {output_path}")
                return output_path
        if "task_result" in result:
            images = result["task_result"].get("images", [])
            if images and images[0].get("url"):
                img = requests.get(images[0]["url"], timeout=60)
                with open(output_path, "wb") as f:
                    f.write(img.content)
                return output_path
        json_path = output_path.replace(".png", ".json")
        with open(json_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return json_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--output", "-o")
    parser.add_argument("--config", default="/workspace/image_api_config.json")
    args = parser.parse_args()
    with open(args.config) as f:
        config = json.load(f)
    gen = ImageGenerator(config)
    result = gen.generate(args.prompt, args.size, args.output)
    print(f"\n完成！" if result else "\n失败！")