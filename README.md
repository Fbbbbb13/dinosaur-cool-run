# 恐龙酷跑游戏 (Dinosaur Cool Run)

一个使用Python和Pygame开发的经典恐龙跑酷游戏，灵感来源于Chrome浏览器的离线小恐龙游戏。

## 游戏特色

- 🦕 可爱的像素风恐龙角色
- 🌵 随机生成的仙人掌障碍物
- 🌙 日夜场景切换
- 🎵 丰富的音效系统
- 📊 实时分数统计
- 🎮 简单易上手的操作

## 游戏截图

游戏包含白天和夜晚两种场景模式，随着游戏进行会自动切换。

## 安装要求

- Python 3.6+
- Pygame库

## 安装步骤

1. 克隆或下载项目到本地

```bash
git clone <repository-url>
cd dinosaur-cool-run-master
```

2. 安装Pygame依赖

```bash
pip install pygame
```

## 运行游戏

```bash
python dinasaur.py
```

## 游戏操作

- **空格键** 或 **上箭头键**: 恐龙跳跃
- **ESC键**: 退出游戏
- **R键**: 游戏结束后重新开始

## 游戏规则

1. 控制小恐龙跳跃躲避仙人掌障碍物
2. 成功躲避障碍物可获得分数
3. 撞到障碍物游戏结束
4. 随着分数增加，游戏速度会逐渐提升
5. 达到一定分数后会切换到夜晚模式

## 项目结构

```
dinosaur-cool-run-master/
├── dinasaur.py          # 主游戏文件
├── README.md            # 项目说明文档
├── audio/               # 音效文件夹
│   ├── bump.wav         # 碰撞音效
│   ├── hit.ogg          # 撞击音效
│   ├── jump.wav         # 跳跃音效
│   ├── point.ogg        # 得分音效
│   ├── score.wav        # 分数音效
│   └── wing.ogg         # 翅膀音效
└── image/               # 图片资源文件夹
    ├── 0.png-9.png      # 数字图片(0-9)
    ├── bg_light.png     # 白天背景
    ├── bg_night.png     # 夜晚背景
    ├── cacti.png        # 仙人掌障碍物
    ├── dinosaur1.png    # 恐龙动画帧1
    ├── dinosaur2.png    # 恐龙动画帧2
    ├── dinosaur3.png    # 恐龙动画帧3
    ├── gameover.png     # 游戏结束画面
    └── stone.png        # 石头障碍物
```

## 技术实现

- **游戏引擎**: Pygame
- **图形渲染**: 2D精灵动画
- **音效系统**: Pygame音频模块
- **碰撞检测**: 矩形碰撞检测
- **动画系统**: 帧动画切换

## 游戏机制

- 恐龙具有跑步动画效果
- 障碍物随机生成，包括仙人掌和石头
- 背景无限滚动效果
- 分数系统和难度递增
- 游戏结束后可重新开始

## 开发说明

这是一个适合Python初学者学习的游戏项目，涵盖了：

- 面向对象编程
- 游戏循环设计
- 事件处理
- 图形渲染
- 音效播放
- 碰撞检测

## 许可证

本项目仅供学习和娱乐使用。

## 贡献

欢迎提交Issue和Pull Request来改进游戏！

---

享受游戏吧！🎮
