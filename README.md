# 500t 门式起重机 · 交互式科普页

豫工 YUGONG 500t 门式起重机（龙门吊）科普交付物：电影感 UI 的单文件交互页 + 滚动运镜穿越页 + 白模 3D 模型。

- **在线演示**：<https://ygtemple.github.io/yugong-500t-crane-explainer/>
- **桌面端体验最佳**：Chrome / Edge，建议开启显卡加速（3D 与沉浸式穿越区才正常显影）

## 页面入口

| 文件 | 说明 |
| --- | --- |
| `index.html` | 站点入口，自动跳转到主页面（GitHub Pages 首页用） |
| `500t门机交互科普页.html` | 主交付物。全部内容、样式、脚本、白模 GLB 内联在这一个文件里 |
| `scroll-tour/index.html` | 沉浸式滚动穿越页，主页面底部「进入沉浸式穿越」跳转至此 |
| `说明书.html` | 使用与演示说明 |
| `先看这里.txt` | 三步上手提示 |

## 目录结构

```
500t门机交互科普页.html      主页面（单文件交付）
说明书.html                  使用说明
index.html                   入口跳转页
assets/                      主页面图片与 30s 宣传视频
scroll-tour/                 沉浸式穿越页
  index.html
  scrub-engine.js            滚动擦除引擎
  assets/stills/             六段静帧
  assets/vid30/              分段运镜视频（桌面 leg / 手机 mobile）
模型源文件/
  director_crane.glb         白模模型
  build_director_crane.py    模型生成脚本
```

**保持 `assets/`、`scroll-tour/` 与主页面同级**，改名或移动会裂图。

## 本地运行

```bash
python -m http.server 8000
```

- 主页面：<http://127.0.0.1:8000/500t门机交互科普页.html>
- 手机第一人称取景：点导演台工具栏「手机取景」出二维码，手机连同一 Wi-Fi 后访问
  `http://<本机IP>:8000/500t门机交互科普页.html#phone`

## 部署

仓库根目录即站点根目录，GitHub Pages 直接按分支发布（`main` / `/`），无需构建步骤。
