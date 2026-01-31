import os, time, pyotp
from playwright.sync_api import sync_playwright

def run():
    un = os.environ.get('GH_USERNAME')
    pw = os.environ.get('GH_PASSWORD')
    # 这里就是你拿到的那串 16 位密钥
    otp_secret = os.environ.get('GH_2FA_SECRET', '').replace(' ', '')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        try:
            print("🚀 开始登录 ClawCloud...")
            page.goto("https://console.run.claw.cloud/login")
            
            # 点击 GitHub 登录
            page.click('button:has-text("GitHub"), a:has-text("GitHub")')
            time.sleep(5)

            # 如果没登录 GitHub，执行登录
            if "github.com/login" in page.url:
                print("📝 正在输入 GitHub 账号密码...")
                page.fill('input[name="login"]', un)
                page.fill('input[name="password"]', pw)
                page.click('input[type="submit"]')
                time.sleep(5)

            # 【核心修复】：处理 2FA
            if "two-factor" in page.url:
                print("⚠️ 检测到 2FA 验证...")
                
                # 如果页面卡在“手机推送”模式，强行切换
                try:
                    print("🔄 尝试切换到验证码输入模式...")
                    # 点击“使用其他方式”或“更多选项”
                    page.click('button:has-text("More options"), .Button-label:has-text("More options")', timeout=5000)
                    time.sleep(2)
                    # 点击“使用验证码 App”
                    page.click('button:has-text("Use an authentication app")')
                    time.sleep(2)
                except:
                    print("ℹ️ 已经是验证码模式或切换失败，尝试直接填码")

                # 使用你的 16 位密钥计算 6 位验证码
                totp = pyotp.TOTP(otp_secret)
                token = totp.now()
                print(f"🔢 自动生成验证码: {token}")

                # 填入验证码
                page.fill('input[autocomplete="one-time-code"], input[name="app_otp"]', token)
                page.keyboard.press("Enter")
                time.sleep(10)

            # 最后的授权页面
            if "authorize" in page.url:
                print("🔘 点击 GitHub 授权按钮...")
                page.click('button[name="authorize"]')
                time.sleep(10)

            if "claw.cloud" in page.url and "signin" not in page.url:
                print("🎉 ✅ 恭喜！登录成功，保活完成！")
            else:
                print(f"❌ 登录失败，当前 URL: {page.url}")
                page.screenshot(path="error.png")
                raise Exception("最终验证失败")

        except Exception as e:
            print(f"💥 运行中出错: {e}")
            page.screenshot(path="error.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run()
