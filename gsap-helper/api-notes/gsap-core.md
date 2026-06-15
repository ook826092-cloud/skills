# GSAP Core 笔记

GSAP 最常用的方法包括：

1. `gsap.to()`
2. `gsap.from()`
3. `gsap.fromTo()`
4. `gsap.set()`
5. `gsap.timeline()`

## gsap.to()

把元素从当前状态动画到目标状态。

```js
gsap.to(".box", {
  x: 100,
  opacity: 1,
  duration: 1,
  ease: "power2.out"
});
```

## gsap.from()

从指定状态动画到当前状态。

```js
gsap.from(".box", {
  y: 50,
  opacity: 0,
  duration: 1,
  ease: "power3.out"
});
```

## gsap.fromTo()

明确指定开始状态和结束状态。

```js
gsap.fromTo(".box",
  {
    y: 60,
    opacity: 0
  },
  {
    y: 0,
    opacity: 1,
    duration: 1,
    ease: "power3.out"
  }
);
```

## gsap.set()

立即设置状态，没有动画。

```js
gsap.set(".box", {
  opacity: 0,
  y: 60
});
```

适合用来设置初始状态，避免页面闪烁。

## 常用属性

```js
x: 100
y: 100
scale: 1.2
rotation: 45
opacity: 0
duration: 1
delay: 0.2
ease: "power3.out"
```
