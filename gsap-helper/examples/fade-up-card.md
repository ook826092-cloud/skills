# 卡片从下往上淡入

适合场景：

- 首页卡片入场
- 弹窗内容出现
- 商品卡片显示
- 个人资料卡片展示

## 完整示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GSAP 卡片淡入动画</title>

  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f3f5f8;
      font-family: Arial, sans-serif;
    }

    .card {
      width: min(90vw, 360px);
      padding: 28px;
      border-radius: 18px;
      background: #ffffff;
      box-shadow: 0 20px 60px rgba(15, 23, 42, 0.16);
      opacity: 0;
      transform: translateY(60px);
    }

    .card h2 {
      margin: 0 0 12px;
      color: #111827;
      font-size: 24px;
    }

    .card p {
      margin: 0 0 20px;
      color: #4b5563;
      line-height: 1.7;
      font-size: 15px;
    }

    .card button {
      width: 100%;
      height: 44px;
      border: none;
      border-radius: 12px;
      background: #2563eb;
      color: #ffffff;
      font-size: 15px;
      cursor: pointer;
    }
  </style>
</head>
<body>

  <div class="card">
    <h2>GSAP 动画卡片</h2>
    <p>
      这个卡片会在页面加载后从下往上淡入，适合内容区、弹窗和列表项入场。
    </p>
    <button>开始使用</button>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>

  <script>
    gsap.to(".card", {
      y: 0,
      opacity: 1,
      duration: 0.9,
      ease: "power3.out",
      delay: 0.2
    });
  </script>

</body>
</html>
```

## 说明

CSS 中先设置：

```css
opacity: 0;
transform: translateY(60px);
```

GSAP 中再动画到：

```js
y: 0,
opacity: 1
```

这样可以避免页面加载时元素闪一下。
