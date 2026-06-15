# Stagger 列表错位动画

stagger 适合多个元素依次出现。

## 示例

```html
<ul class="list">
  <li>项目一</li>
  <li>项目二</li>
  <li>项目三</li>
  <li>项目四</li>
</ul>

<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>

<script>
  gsap.set(".list li", {
    y: 30,
    opacity: 0
  });

  gsap.to(".list li", {
    y: 0,
    opacity: 1,
    duration: 0.6,
    ease: "power3.out",
    stagger: 0.12
  });
</script>
```

## 说明

```js
stagger: 0.12
```

表示每个列表项之间间隔 0.12 秒开始播放。

也可以写成对象：

```js
stagger: {
  each: 0.12,
  from: "start"
}
```

从中间向两边播放：

```js
stagger: {
  each: 0.1,
  from: "center"
}
```
