# GSAP 常见问题和避坑

## 1. 页面加载时元素闪一下

原因：HTML 先渲染出元素，GSAP 后执行，导致元素短暂显示。

解决方式一：CSS 设置初始状态。

```css
.card {
  opacity: 0;
  transform: translateY(60px);
}
```

然后 GSAP 动画到正常状态：

```js
gsap.to(".card", {
  y: 0,
  opacity: 1
});
```

解决方式二：使用 `gsap.set()`。

```js
gsap.set(".card", {
  y: 60,
  opacity: 0
});

gsap.to(".card", {
  y: 0,
  opacity: 1
});
```

## 2. ScrollTrigger 不生效

检查：

1. 是否引入了 ScrollTrigger 文件
2. 是否执行了 `gsap.registerPlugin(ScrollTrigger)`
3. trigger 选择器是否正确
4. 页面是否真的可以滚动
5. start/end 是否设置合理

## 3. 动画太生硬

可以换 ease：

```js
ease: "power3.out"
```

弹性效果：

```js
ease: "back.out(1.5)"
```

滚动跟随动画：

```js
ease: "none"
```

## 4. 多个动画顺序混乱

如果动画有明确先后顺序，优先用 Timeline：

```js
const tl = gsap.timeline();

tl.to(".one", {
  opacity: 1
});

tl.to(".two", {
  opacity: 1
});
```

## 5. 列表动画代码重复

不要手动给每个元素写一遍动画，优先使用 stagger：

```js
gsap.to(".item", {
  y: 0,
  opacity: 1,
  stagger: 0.1
});
```

## 6. hover 动画抖动

如果 hover 频繁触发，可以使用 overwrite：

```js
gsap.to(".btn", {
  scale: 1.05,
  duration: 0.25,
  overwrite: true
});
```

## 7. 使用 scrub 时动画有缓动延迟

滚动跟随动画通常使用：

```js
ease: "none"
```

示例：

```js
gsap.to(".box", {
  x: 300,
  ease: "none",
  scrollTrigger: {
    trigger: ".box",
    scrub: true
  }
});
```
