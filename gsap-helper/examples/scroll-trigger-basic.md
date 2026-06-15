# ScrollTrigger 滚动触发动画

ScrollTrigger 用于滚动到某个位置时触发动画。

## 完整示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ScrollTrigger 示例</title>

  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f8fafc;
    }

    .space {
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #64748b;
      font-size: 24px;
    }

    .section {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .card {
      width: min(90vw, 420px);
      padding: 32px;
      border-radius: 20px;
      background: white;
      box-shadow: 0 24px 70px rgba(15, 23, 42, 0.16);
      opacity: 0;
      transform: translateY(80px);
    }

    .card h2 {
      margin: 0 0 12px;
      color: #111827;
    }

    .card p {
      margin: 0;
      color: #4b5563;
      line-height: 1.7;
    }
  </style>
</head>
<body>

  <div class="space">向下滚动</div>

  <section class="section">
    <div class="card">
      <h2>滚动触发卡片</h2>
      <p>当这个卡片进入视口时，GSAP 会触发从下往上淡入动画。</p>
    </div>
  </section>

  <div class="space">结束</div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>

  <script>
    gsap.registerPlugin(ScrollTrigger);

    gsap.to(".card", {
      y: 0,
      opacity: 1,
      duration: 0.9,
      ease: "power3.out",
      scrollTrigger: {
        trigger: ".card",
        start: "top 80%",
        toggleActions: "play none none reverse"
      }
    });
  </script>

</body>
</html>
```

## 参数说明

```js
start: "top 80%"
```

表示当 `.card` 的顶部到达视口 80% 的位置时触发。

```js
toggleActions: "play none none reverse"
```

表示：

1. 进入时播放
2. 离开时不处理
3. 重新进入时不处理
4. 向上滚回去时反向播放
