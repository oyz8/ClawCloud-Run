# [⭐最近申请公益领域需要100星，帮我另一个项目点一Star ⭐ ](https://github.com/oyz8/random-pic-api) Star 星星走起 动动发财手点点

> 🚀 基于 Selenium 的 ClawCloud 自动登录保活脚本，专为青龙面板设计，支持 GitHub OAuth 登录、两步验证、Cookie 自动更新。

## ✨ 功能特性

- 🔐 **GitHub OAuth 登录** - 自动完成 GitHub 授权登录流程
- 📱 **两步验证支持** - 支持 GitHub Mobile 和 TOTP 验证码
- 🔄 **Cookie 自动更新** - 登录后自动更新青龙环境变量中的 Cookie
- 📸 **截图记录** - 关键步骤自动截图，方便调试
- 📬 **Telegram 通知** - 实时推送登录状态和验证请求
- 🛡️ **设备验证处理** - 自动等待并处理设备验证
- ♻️ **保活访问** - 登录后自动访问控制台保持活跃

![Mobile登录](./img/Mobile登录.png)
![2FA登录](./img/2FA登录.png)
![Cookie自动登录](./img/Cookie自动登录.png)


## 📋 环境要求

### 系统依赖

- Python 3.8+
- Chromium 浏览器
- ChromeDriver

### Python 依赖

```
selenium
requests
```

## 🔧 安装步骤

### 青龙面板安装

#### 1. 添加 Linux 依赖

在 **依赖管理 → Linux** 中添加：

```
chromium
chromium-chromedriver
```
![依赖](./img/青龙面板添加 Linux 依赖.png)


或 SSH 进入容器执行：

```bash
apk add chromium chromium-chromedriver
```
![依赖](./img/进入容器添加 Linux 依赖.png)


#### 2. 添加 Python 依赖

在 **依赖管理 → Python3** 中添加：

```
selenium
requests
```
![依赖](./img/青龙面板添加 Python 依赖.png)


#### 3. 创建青龙应用

1. 进入 **青龙面板 → 系统设置 → 应用设置**
2. 点击 **添加应用**
3. 填写名称（如：ClawCloud）
4. 权限选择 **环境变量**
5. 保存后复制 `Client ID` 和 `Client Secret`

![青龙应用](./img/创建青龙面板应用.png)


#### 4. 添加环境变量

在 **环境变量** 中添加以下变量：

| 变量名 | 说明 | 必填 | 示例 |
|--------|------|:----:|------|
| `GH_USERNAME` | GitHub 用户名 | ✅ | `your_username` |
| `GH_PASSWORD` | GitHub 密码 | ✅ | `your_password` |
| `GH_SESSION` | GitHub Cookie（自动更新） | ❌ | 首次运行后自动填充 |
| `TG_BOT_TOKEN` | Telegram Bot Token | ✅ | `123456:ABC-DEF...` |
| `TG_CHAT_ID` | Telegram Chat ID | ✅ | `123456789` |
| `QL_CLIENT_ID` | 青龙应用 Client ID | ✅ | `xxx` |
| `QL_CLIENT_SECRET` | 青龙应用 Client Secret | ✅ | `xxx` |
| `TWO_FACTOR_WAIT` | 2FA 等待时间（秒） | ❌ | `120` |

![环境变量](./img/青龙面板添加环境变量.png)

#### 5. 添加定时任务

1. 进入 **定时任务 → 添加任务**
2. 填写信息：
   - **名称**：ClawCloud 自动登录
   - **命令**：`task clawcloud_login.py`
   - **定时规则**：`0 8 */3 * *`（每3天早上8点执行）

## 📖 使用说明

### 首次运行

1. 确保所有环境变量已正确配置
2. 手动运行一次脚本
3. 根据 Telegram 通知完成验证（如需要）
4. 脚本会自动保存 Cookie 到环境变量

### 两步验证

#### GitHub Mobile

1. 收到 Telegram 通知后，打开手机 GitHub App
2. 确认显示的数字与截图一致
3. 点击批准

#### TOTP 验证码

1. 收到 Telegram 通知后，打开验证器 App
2. 获取 6 位验证码
3. 在 Telegram 中发送：`/code 123456`

### 设备验证

1. 收到 Telegram 通知后
2. 检查邮箱并点击验证链接
3. 或在 GitHub App 中批准

## 📁 项目结构

```
clawcloud-ql/
├── clawcloud_login.py    # 主脚本
└── README.md             # 说明文档
```

## ⚙️ 配置说明

### ClawCloud 地址

根据你的账号区域修改 `CLAW_CLOUD_URL`：

| 区域 | 地址 |
|------|------|
| 默认 | `https://console.run.claw.cloud` |
| 欧洲 | `https://eu-central-1.run.claw.cloud` |
| 美国 | `https://us-east-1.run.claw.cloud` |
| 亚洲 | `https://ap-southeast-1.run.claw.cloud` |

### 改进区域自动切换

脚本会自动跟踪 OAuth 回调后的实际区域。例如：
- 初始访问 `eu-central-1` 区域
- OAuth 回调可能跳转到 `ap-southeast-1` 区域
- 脚本会自动使用实际区域进行后续操作

这意味着 `CLAW_CLOUD_URL` 只需要设置初始登录入口，无需担心区域跳转问题。

### Telegram Bot 配置

1. 在 Telegram 中找到 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建机器人
3. 获取 Bot Token
4. 发送 `/start` 给你的机器人
5. 访问 `https://api.telegram.org/bot<TOKEN>/getUpdates` 获取 Chat ID

## 🔍 运行日志示例

```
============================================================
🚀 ClawCloud 自动登录
============================================================

ℹ️ GitHub 用户名: abc
ℹ️ 现有 Session: 无
ℹ️ 青龙面板 API: 已配置
ℹ️ Telegram 通知: 已配置
✅ Chrome 浏览器驱动初始化成功
🔹 步骤 1: 访问 ClawCloud
ℹ️ 当前页面类型: signin
🔹 步骤 2: 点击 GitHub 登录
✅ 已点击: GitHub 登录
🔹 步骤 3: 处理认证流程
ℹ️ 认证循环 [1/5]
ℹ️ 页面类型: github_login
ℹ️ GitHub 流程处理 [1/3]: github_login
🔹 登录 GitHub...
✅ GitHub 凭据已输入
⚠️ 需要两步验证（GitHub Mobile），等待 120 秒...
ℹ️ 等待中... (10/120秒)
✅ 两步验证通过！
ℹ️ GitHub 流程处理 [2/3]: callback
ℹ️ 认证循环 [2/5]
ℹ️ 页面类型: callback
🔹 等待 OAuth callback 处理完成...
ℹ️ [0s] 页面类型: callback, URL: https://eu-central-1.run.claw.cloud/callback?code=1cacfccef1...
ℹ️ Callback 仍在处理中... (5/30秒)
ℹ️ [9s] 页面类型: console, URL: https://eu-central-1.run.claw.cloud/...
✅ Callback 处理完成，已进入控制台！
🔹 步骤 4: 验证登录结果
ℹ️ 验证URL: https://eu-central-1.run.claw.cloud/
✅ 登录验证成功！
🔹 执行保活操作...
✅ 已访问: 应用页面
🔹 步骤 5: 更新 Cookie
✅ 新 Cookie: Nm.......FP5
✅ 环境变量 GH_SESSION 更新成功

============================================================
✅ 执行成功！
============================================================

```

## ❓ 常见问题

### Q: 提示 "找不到 GitHub 按钮"

**A:** ClawCloud 页面可能有更新，请检查：
1. `CLAW_CLOUD_URL` 是否正确
2. 手动访问登录页确认按钮存在
3. 提交 Issue 反馈

### Q: 提示 "WebDriver 初始化失败"

**A:** 检查 Chromium 是否正确安装：
```bash
# 进入青龙容器
docker exec -it qinglong bash

# 检查 Chromium
which chromium-browser
chromium-browser --version

# 检查 ChromeDriver
which chromedriver
chromedriver --version
```

### Q: Cookie 无法自动更新

**A:** 检查：
1. 青龙应用权限是否包含 "环境变量"
2. `QL_CLIENT_ID` 和 `QL_CLIENT_SECRET` 是否正确
3. 青龙面板 API 是否正常

### Q: 两步验证超时

**A:** 
1. 增加等待时间：设置环境变量 `TWO_FACTOR_WAIT=180`
2. 确保手机能及时收到通知
3. 检查 Telegram 通知是否正常

### Q: 设备验证失败

**A:**
1. 检查 GitHub 绑定的邮箱
2. 确保能及时处理验证邮件
3. 或在 GitHub App 中预先批准设备

## 📝 更新日志

### v1.0.0 (2024-12-31)

- ✨ 初始版本发布
- 🔐 支持 GitHub OAuth 登录
- 📱 支持两步验证（Mobile/TOTP）
- 🔄 Cookie 自动更新到青龙环境变量
- 📬 Telegram 通知集成

## ⚠️ 免责声明

- 本脚本仅供学习交流使用
- 请勿用于任何违反服务条款的行为
- 使用本脚本产生的任何后果由使用者自行承担
- 建议定期检查账号状态，确保服务正常

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

---


