# Timeline 笔记

Timeline 用于管理多个动画的播放顺序。

## 基础写法

```js
const tl = gsap.timeline();

tl.to(".one", {
  x: 100,
  duration: 1
});

tl.to(".two", {
  y: 100,
  duration: 1
});
```

## defaults

可以统一设置默认参数：

```js
const tl = gsap.timeline({
  defaults: {
    duration: 0.6,
    ease: "power3.out"
  }
});
```

## 位置参数

正常顺序：

```js
tl.to(".box", {
  x: 100
});
```

提前 0.3 秒开始：

```js
tl.to(".box", {
  opacity: 1
}, "-=0.3");
```

延后 0.2 秒开始：

```js
tl.to(".box", {
  scale: 1
}, "+=0.2");
```

和上一段同时开始：

```js
tl.to(".box", {
  rotation: 360
}, "<");
```

在上一段结束时开始：

```js
tl.to(".box", {
  opacity: 0
}, ">");
```

## 暂停与播放

```js
const tl = gsap.timeline({
  paused: true
});

tl.play();
tl.pause();
tl.reverse();
tl.restart();
```
