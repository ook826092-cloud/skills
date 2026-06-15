# 按钮交互动效

适合按钮 hover、点击反馈、弹性缩放。

## 示例

```html
<button class="btn">点击按钮</button>

<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>

<script>
  const button = document.querySelector(".btn");

  button.addEventListener("mouseenter", function () {
    gsap.to(button, {
      scale: 1.06,
      duration: 0.25,
      ease: "power2.out",
      overwrite: true
    });
  });

  button.addEventListener("mouseleave", function () {
    gsap.to(button, {
      scale: 1,
      duration: 0.25,
      ease: "power2.out",
      overwrite: true
    });
  });

  button.addEventListener("mousedown", function () {
    gsap.to(button, {
      scale: 0.96,
      duration: 0.12,
      ease: "power2.out",
      overwrite: true
    });
  });

  button.addEventListener("mouseup", function () {
    gsap.to(button, {
      scale: 1.06,
      duration: 0.18,
      ease: "back.out(1.8)",
      overwrite: true
    });
  });
</script>
```

## 说明

按钮交互建议保持轻量，不要加太长的动画时间。

通常 hover 使用 `0.2s ~ 0.3s`，点击反馈使用 `0.1s ~ 0.18s`。
