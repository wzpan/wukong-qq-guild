# wukong-qq-guild

[wukong-robot](http://github.com/wzpan/wukong-robot) 的 QQ 频道机器人客户端。利用这个机器人，可以实现使用 QQ 频道机器人控制 wukong-robot 。

## demo

使用 QQ 扫码加入 wukong-robot 用户交流频道，然后在 🤖一起玩Bot 子频道里体验 wukong-robot 机器人。

![](https://wzpan-1253537070.cos.ap-guangzhou.myqcloud.com/misc/wukong-guild-qrcode.png)

> 注意：demo 机器人的后端连接的是 wukong-robot 的 [demo 后台](http://bot.hahack.com:5000)，因此将无法正常体验拍照、播放音乐的功能。建议自行部署以获得更好的体验。

## 安装

1. 先安装 wukong-robot 并运行，确保 wukong-robot 的版本 >= 2.4.4；
2. 安装依赖：

``` bash
pip3 install -r requirements.txt
```

## 注册频道机器人

如果你需要一个服务你自己的 wukong-robot 后端的频道机器人（通常情况下都应该这么做），那么你需要申请注册并创建一个频道机器人。这里有一份详细的指引：[QQ机器人快速注册指南](https://cloud.tencent.com/lab/lab/console/1005936350069241?channel=p1001&sceneCode=q) 。

> 注意：由于大多数人的 wukong-robot 都是功能比较私密的机器人，因此从安全起见，建议注册为私域机器人，并把控好机器人所在的频道成员。例如，对于接入了 [HASS](https://wukong.hahack.com/#/contrib?id=hass) 技能的 wukong-robot ，所关联的频道应该只开放给亲朋好友 —— 你肯定不希望线上的陌生人都能够开关你家的灯。

## 配置机器人指令

处于方便起见，可以在[机器人管理端](https://q.qq.com/bot/)的 [发布设置] -> [[功能配置](https://q.qq.com/bot/#/developer/publish-config/function-config)] 里，给机器人客户端添加如下一些常用指令：

![指令集](https://wzpan-1253537070.cos.ap-guangzhou.myqcloud.com/misc/commands.jpeg)

> tips：如果你有其他常用的交互语句，当然也可以添加到指令集里。这些指令会把去掉第一个 `/` 后的内容原封不动地传给 wukong-robot 进行交互。

## 配置机器人

``` bash
cp config.example.yml config.yml
```

然后编辑 config.yml 。尤其注意如果频道机器人和 wukong-robot 并不在同一台服务器上运行，务必修改 `host` 配置。

## 运行

``` bash
python3 bot.py
```
## 使用

与 wukong-robot 聊天，文本或者语音都将会作为指令转发给 wukong-robot 的后台管理端。