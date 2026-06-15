# Timeline 基础动画

Timeline 适合多个元素按顺序播放动画。

## 示例

```html
<div class="hero">
  <h1 class="title">欢迎使用 GSAP</h1>
  <p class="desc">用时间线管理复杂动画会更清晰。</p>
  <button class="btn">开始体验</button>
</div>

<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>

<script>
  gsap.set([".title", ".desc", ".btn"], {
    y: 40,
    opacity: 0
  });

  const tl = gsap.timeline({
    defaults: {
      duration: 0.7,
      ease: "power3.out"
    }
  });

  tl.to(".title", {
    y: 0,
    opacity: 1
  });

  tl.to(".desc", {
    y: 0,
    opacity: 1
  }, "-=0.35");

  tl.to(".btn", {
    y: 0,
    opacity: 1
  }, "-=0.3");
</script>
```

## 关键点

`defaults` 可以统一设置每一段动画的默认参数：

```js
const tl = gsap.timeline({
  defaults: {
    duration: 0.7,
    ease: "power3.out"
  }
});
```

`"-=0.3"` 表示当前动画提前 0.3 秒开始，和上一段动画有重叠。
