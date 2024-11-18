<!-- markdownlint-disable MD026 MD031 MD033 MD036 MD041 MD046 MD051 MD050-->
<div align="center">
  <img src="https://raw.githubusercontent.com/Agnes4m/nonebot_plugin_l4d2_server/main/image/logo.png" width="180" height="180"  alt="AgnesDigitalLogo">
  <br>
  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

__✨基于nonebot2框架的插件，实现交互游戏恶魔轮盘赌✨__

<a href="https://github.com/Agnes4m/nonebot_plugin_BR/stargazers">
        <img alt="GitHub stars" src="https://img.shields.io/github/stars/Agnes4m/nonebot_plugin_BR" alt="stars">
</a>
<a href="https://github.com/Agnes4m/nonebot_plugin_BR/issues">
        <img alt="GitHub issues" src="https://img.shields.io/github/issues/Agnes4m/nonebot_plugin_BR" alt="issues">
</a>
<a href="https://jq.qq.com/?_wv=1027&k=HdjoCcAe">
        <img src="https://img.shields.io/badge/QQ%E7%BE%A4-399365126-orange?style=flat-square" alt="QQ Chat Group">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_BR">
        <img src="https://img.shields.io/pypi/v/nonebot_plugin_BR.svg" alt="pypi">
</a>
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
    <img src="https://img.shields.io/badge/nonebot-2.1.0+-red.svg" alt="NoneBot">
</div>

## 说明

本项目用于以交互形式完成游戏玩法恶魔轮盘赌(Buckshot Roulette)的玩法，可以在群聊中使用，一个群同时只能存在一场对局

由于“赌”在国内部分平台是被封禁的，所以文案均改为“恶魔轮盘”

## 安装

以下提到的方法 任选**其一**即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot_plugin_BR
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot_plugin_BR
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot_plugin_BR
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot_plugin_BR
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot_plugin_BR
```

</details>
</details>

## 指令

### 游戏外

- br开始| br加入 —— 开始游戏
- br help —— 查看帮助

### 游戏中

- 开枪 —— (前提:加入游戏)进行攻击判定
- 结束游戏 —— (前提:在对局中,或者超级管理员)结束当前会话在进行的游戏
- 使用道具 xxx(目前道具：刀 | 手铐 | 香烟 | 放大镜 | 饮料 )
- br当前状态 —— 查看当前游戏的数值状态

## 测试图

![测试图1](./img/test2.png)
![测试图2](./img/test1.png)

## env配置

暂无

## QA

### 重启后加入游戏方法

在游戏结束后，可以通过命令`br加入`加入游戏，两个人都需要发送，否则判断不在游戏中

### 饮料退弹效果

饮料退弹应该是不可知的子弹，但是当开枪后的效果结算就知道当前的子弹，这是一个bug

## to do

- [x] 开枪基本逻辑
- [x] 道具逻辑
- [ ] 分数逻辑
- [ ] 人机逻辑

## 🙈 其他

- 本项目仅供学习使用，请勿用于商业用途，喜欢该项目可以Star或者提供PR
- [爱发电](https://ifdian.net/a/agnes_digital/plan)
- [加入群聊](https://jq.qq.com/?_wv=1027&k=HdjoCcAe)
