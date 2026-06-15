# ScrollTrigger 笔记

ScrollTrigger 用于滚动触发动画。

## 引入

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
```

## 注册插件

```js
gsap.registerPlugin(ScrollTrigger);
```

## 基础写法

```js
gsap.to(".box", {
  x: 300,
  scrollTrigger: {
    trigger: ".box",
    start: "top 80%",
    end: "bottom 20%",
    toggleActions: "play none none reverse"
  }
});
```

## scrub

让动画进度跟随滚动条：

```js
gsap.to(".box", {
  x: 300,
  ease: "none",
  scrollTrigger: {
    trigger: ".box",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});
```

## pin

固定元素：

```js
ScrollTrigger.create({
  trigger: ".section",
  start: "top top",
  end: "+=1000",
  pin: true
});
```

## markers

调试触发位置：

```js
scrollTrigger: {
  trigger: ".box",
  start: "top 80%",
  markers: true
}
```

正式上线前建议删除：

```js
markers: true
```

## refresh

如果页面图片加载后高度变化，可以刷新：

```js
ScrollTrigger.refresh();
```
